import discord
from discord.ext import commands   
import time


class RequestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.hybrid_command(name="shop_request")
    async def shop_request(self, ctx: commands.Context, item_name: str, quantity: int, *, notes: str = None):
        
        if ctx.interaction:
            await ctx.interaction.response.defer(ephemeral=True)
        else:
            await ctx.defer()

        if quantity <= 0:
            await ctx.send("Please provide a valid quantity greater than 0.", ephemeral=True)
            return
        
        await ctx.send("Your shop request has been submitted.", ephemeral=True)

        embed = discord.Embed(
            title="New Shop Request",
            description=f"**Item Name:** {item_name}\n**Quantity:** {quantity}\n**Notes:** {ctx.author.mention}",
            color=discord.Color.from_str("#ffb4f1"),
        )

        if notes:
            embed.add_field(name="Notes", value=notes)

        embed.set_footer(text=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), icon_url=ctx.author.avatar.url)
        channel = self.bot.get_channel(1322481571995062332)
        await channel.send(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(RequestCommands(bot))