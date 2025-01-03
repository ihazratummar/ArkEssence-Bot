import discord
from discord.ext import commands   
import time
from ..helper_function import Shop_Request_Modal


class RequestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.hybrid_command(name="shop_request")
    async def shop_request(self, ctx: commands.Context):
        
        if ctx.interaction:
            await ctx.interaction.response.send_modal(Shop_Request_Modal())
        else:
            await ctx.defer()
        
async def setup(bot: commands.Bot):
    await bot.add_cog(RequestCommands(bot))



