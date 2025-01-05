import discord
from discord.ext import commands
from config import Bot


class Help(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @commands.hybrid_command(name="help")
    async def help(self, ctx: commands.Context):
        """Display all the commands Available"""

        embed= discord.Embed(
            title="Ark Essence",
            description="List of all the commands available",
            color=discord.Color.from_str("#ffb4f1")
        )

        for c in self.bot.cogs:
            cog = self.bot.get_cog(c)
            if any(cog.walk_commands()):
                embed.add_field(name=cog.qualified_name, value=" , ".join(f"`/{i.name}`" for i in cog.walk_commands()), inline= False)


        await ctx.send(embed= embed)

    @commands.hybrid_command(name="vault-help")
    async def vault_help(self, context: commands.Context):
        """Get the Vault Command List"""
        embed = discord.Embed(
            title= "Vault Help",
            description= f"Use the vault command only in the <#{1015764336221900870}>\nCheck the available commands",
            color= discord.Color.from_str("#ffb4f1")
            )
        embed.add_field(name="> **/claim-vault** ", value=">>> Claim your vault to stat using our shop")
        embed.add_field(name="> **/myvault** ", value=">>> To check your vault information")
        embed.add_field(name="> **/vaults** ", value=">>> Check available vaults")

        await context.send(embed=embed)

    


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
    