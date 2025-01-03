import discord
from discord.ext import commands
from ..helper_function import ReportView


class Essence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="report")
    async def report(self, ctx: discord.Interaction):
        view = ReportView()  
        await ctx.send("Select a report type:", view=view)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Essence(bot))
    bot.add_view(ReportView()) 