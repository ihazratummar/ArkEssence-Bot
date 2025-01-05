import json
import random
import constants
import  discord
from discord.ext import commands
from config import Bot

class Vaults(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.database
        self.collection = self.db["user_data"]  # Existing user data collection

        # Load or initialize vaults list from JSON file
        self.vaults_file = "data/vaults.json"
        self.vaults = self._load_vaults()

    def is_allowed_channel_or_admin(allowed_channel):
        async def predicate(ctx: commands.Context):
            return(ctx.author.guild_permissions.administrator or ctx.channel.id in allowed_channel)
        return commands.check(predicate)

    def _load_vaults(self):
        """Load vaults from a JSON file or initialize them if the file does not exist."""
        try:
            with open(self.vaults_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            vaults = [
                {"vault_number": i, "status": "available", "assigned_to": None, "pin": None}
                for i in range(1, 13)
            ]
            self._save_vaults(vaults)
            return vaults

    def _save_vaults(self, vaults):
        """Save the current vaults list to the JSON file."""
        with open(self.vaults_file, "w") as file:
            json.dump(vaults, file, indent=4)

    def _update_vault(self, vault_number, status, assigned_to=None, pin=None):
        """Update a specific vault in the vaults list and save to the JSON file."""
        for vault in self.vaults:
            if vault["vault_number"] == vault_number:
                vault["status"] = status
                vault["assigned_to"] = assigned_to
                vault["pin"] = pin
                self._save_vaults(self.vaults)
                return

    def is_user_vault_exist(self, user_id) -> bool:
        """Check if a user already has a vault assigned."""
        user_data = self.collection.find_one({"_id": str(user_id)})
        if user_data is None:
            return False  # User does not exist in the collection

        # Safely access the 'vault_number' field
        return user_data.get("vault_number") is not None

    def clear_vault_by_id(self, vault_id):
        user_data = self.collection.find_one({"vault_number": vault_id})

        if not user_data:
            return False

        user_id = user_data.get("_id")

        self._update_vault(vault_number=vault_id, status="available", assigned_to=None, pin= None)
        self.collection.update_one(
            {"_id": user_id},
            {"$unset": {"vault_number": None, "pin": None}}
        )


    @commands.hybrid_command("claim-vault")
    async def claimvault(self, ctx: commands.Context):

        if self.is_user_vault_exist(user_id=ctx.author.id):
            await ctx.send("We have assigned you a vault use `/myvault` to check")
            return

        """Allows a player to claim an available vault."""
        available_vaults = [vault for vault in self.vaults if vault["status"] == "available"]

        if not available_vaults:
            await ctx.send("No vaults are currently available.")
            return



        options = [
            discord.SelectOption(label=f"Vault #{v['vault_number']}", value=str(v['vault_number']))
            for v in available_vaults
        ]

        class VaultSelect(discord.ui.Select):
            def __init__(self, vault_list, update_vault, collection, author):
                super().__init__(placeholder="Select a vault to claim", options=vault_list)
                self.update_vault = update_vault
                self.collection = collection
                self.author = author

            async def callback(self, interaction: discord.Interaction):
                if interaction.user != self.author:
                    await interaction.response.send_message("You cannot select a vault for another user.", ephemeral=True)
                    return

                vault_number = int(self.values[0])
                pin = random.randint(1000, 9999)
                self.update_vault(vault_number, "taken", str(interaction.user.id), pin)

                # Update user data in the database
                self.collection.update_one(
                    {"_id": str(interaction.user.id)},
                    {"$set": {"vault_number": vault_number, "pin": pin}},
                    upsert=True
                )

                await interaction.response.send_message(
                    f"Vault #{vault_number} has been assigned to you!\n\nPIN: {pin}\n\nPlease share the PIN only with your trusted tribe members.",
                    ephemeral=True
                )
                self.view.stop()

        view = discord.ui.View()
        view.add_item(VaultSelect(vault_list=options, update_vault= self._update_vault, collection= self.collection, author= ctx.author))
        await ctx.send("Please select a vault to claim:", view=view)

    @commands.hybrid_command("clear-vault")
    @commands.has_permissions(administrator=True)
    async def release_vault(self, ctx: commands.Context, vault_number: int):
        await  ctx.defer()

        vault = next((v for v in self.vaults if v["vault_number"]))

        if not vault:
            await ctx.send(f"Vault #{vault_number} does not exist.")
            return

        self.clear_vault_by_id(vault_id=vault_number)

        await ctx.send(f"Vault #{vault_number} has been cleared and is now available.")

    @commands.hybrid_command("myvault")
    async def myvault(self, ctx: commands.Context):
        """Display the vault assigned to the user."""
        user_data = self.collection.find_one({"_id": str(ctx.author.id)})

        if user_data is None or "vault_number" not in user_data:
            await ctx.send("You do not have a vault assigned.")
            return

        vault_number = user_data["vault_number"]
        vault = next((v for v in self.vaults if v["vault_number"] == vault_number), None)

        if vault is None:
            await ctx.send("Your vault is no longer available.")
            return

        if not ctx.interaction:
            await ctx.send(f"Your vault is: #{vault_number} use `/myvault` to check your pin")
        else:
            await ctx.interaction.response.send_message(f"Your vault is: #{vault_number} and pin is: {user_data['pin']}", ephemeral=True)

    @commands.hybrid_command("vaults")
    @is_allowed_channel_or_admin(allowed_channel=[1015764336221900870])
    async def vaults(self, ctx: commands.Context):
        """Display a list of all vaults and their status."""
        
        embed = discord.Embed(
            title="Vaults",
            description="",
            color=discord.Color.from_str("#ffb4f1")
        )

        for vault in self.vaults:
            status = vault["status"]
            assigned_to = vault["assigned_to"] 
            assigned_Member = ctx.guild.get_member(int(assigned_to)) if status == "taken" else "None"
            
            embed.add_field(name=f"Vault #{vault['vault_number']} " + ("🟢" if status == "available" else "🔴"), value=f">>> Status: {status}\nAssigned to: {assigned_Member}", inline=True)

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Clear the vault assigned to a user when they leave the server."""
        if self.is_user_vault_exist(user_id=member.id):
            user_data = self.collection.find_one({"_id": str(member.id)})
            vault_number = user_data["vault_number"]
            self.clear_vault_by_id(vault_id=vault_number)





async def setup(bot: commands.Bot):
    await  bot.add_cog(Vaults(bot=bot))