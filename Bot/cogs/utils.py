import discord
from discord.ext import commands
from config import Bot


class Utils(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong!')

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

    


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))
    