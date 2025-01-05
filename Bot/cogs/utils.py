import discord
from discord.ext import commands
from config import Bot


class Utils(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong!')


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))
    