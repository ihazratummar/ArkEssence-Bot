import discord
from discord.ext import commands
from cogs.ticket.ticket_button import CreateButton 



class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ticket")
    @commands.has_permissions(administrator=True)
    async def ticket(self, ctx: commands.Context):
        await ctx.defer()

        embed = discord.Embed(
            title="︵‿୨♡୧‿︵ 𓆩♡𓆪 Support Tickets 𓆩♡𓆪 ︵‿୨♡୧‿︵",
            description="""Open an admin support ticket, here is where you can get in game help geared toward things like accidentally leaving your tribe and general support questions""",
              color=discord.Color.from_str("#ffb4f1")  # Replace with your desired hex color
        )
        view = CreateButton()
        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
    bot.add_view(CreateButton())  # Add the view to the bot
    
    