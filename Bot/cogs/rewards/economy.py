import discord
from discord.ext import commands
from config import Bot



class Economy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = bot.database
        self.collection = self.db["user_data"]
        self.bbs_emoji = "<:Berrybush_Seeds:1322750639557709926>"


    @commands.hybrid_command(name="addbbs")
    @commands.has_permissions(manage_messages=True)
    async def addbbs(self, ctx: commands.Context, member: discord.Member = None, amount: int = 0, *, reason: str = None):

        await ctx.defer()

        if member is None:
            member = ctx.author

        if amount <= 0:
            await ctx.send("Please provide a valid amount greater than 0.")
            return

        user_id = str(member.id)
        collection = self.collection

        # Check if the user exists in the database
        user_data = collection.find_one({"_id": user_id})

        if user_data:
            # Increment the "bbs" value for existing users
            bbs = user_data.get("bbs", 0) + amount
            collection.update_one(
                {"_id": user_id},
                {"$inc": {"bbs": amount}}
            )
        else:
            # Add new user with the initial "bbs" value
            bbs = amount
            collection.insert_one({
                "_id": user_id,
                "bbs": bbs,
                "name": member.name
            })

        embed = discord.Embed(
                title=f"{member.display_name} Bushberry Log",
                description=f"︵‿୨♡୧‿︵︵‿୨♡୧‿︵︵‿୨♡୧‿︵",
                color=discord.Color.from_str("#ffb4f1")  # Replace with your desired hex color
            )
        embed.add_field(name="📥Received", value=f"{self.bbs_emoji}{amount}", inline=True)
        embed.add_field(name="🪙Total", value=f"{self.bbs_emoji}{bbs}", inline=True)
        embed.add_field(name="", value="", inline=False)
        embed.set_thumbnail(url=member.avatar._url)
        if reason:
            embed.add_field(name="📜Reason", value=reason, inline=False)

        # DM the user
    
        try:
            await member.send(embed = embed)
        except discord.Forbidden:
            await ctx.send(f"**{member.name}**, I couldn't send you a DM. Please check your settings.")

        # Log in a specific channel
        log_channel_id = 1035354995429736498  # Replace with your log channel ID
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            

            await log_channel.send(embed=embed)

        
        await ctx.send(f"Added <:Berrybush_Seeds:1322750639557709926>{amount} Bushberries to {member.mention}.")


    @commands.hybrid_command(name="resetbbs")
    @commands.has_permissions(manage_messages=True)
    async def reset_bbs(self, ctx: commands.Context, member: discord.Member = None):
        await ctx.defer()

        if member is None:
            member = ctx.author

        user_id = str(member.id)
        collection = self.collection

        # Check if the user exists in the database
        user_data = collection.find_one({"_id": user_id})

        if user_data:
            bbs = user_data.get("bbs", 0)
            collection.update_one(
                {"_id": user_id},
                {"$set": {"bbs": 0}}
            )

            await ctx.send(f"Reset Bushberries for {member.mention}.")
        else:
            await ctx.send(f"{member.mention} doesn't have any Bushberries yet.")

    @commands.hybrid_command("checkbbs")
    async def check_bbs(self, ctx: commands.context):
        user_id = str(ctx.author.id)
        user_data = self.collection.find_one({"_id": user_id})

        if user_data:
            bbs = user_data.get("bbs", 0)
            embed = discord.Embed(
                title="",
                description=f"Your current Bushberries is <:Berrybush_Seeds:1322750639557709926>{bbs}",
                color= discord.Color.from_str("#ffb4f1"),
            )
        else:
            embed = discord.Embed(
                title="",
                description=f"You don't have any Bushberries yet",
                color= discord.Color.from_str("#ffb4f1"),
            )

        await ctx.send(embed = embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))