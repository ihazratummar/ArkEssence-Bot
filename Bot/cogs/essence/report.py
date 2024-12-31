import discord
from discord.ext import commands
import asyncio
import time

class ReportDropDown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Game Issue", value="Game Issue "),
            discord.SelectOption(label="Player Issue", value="Prayer Issue"),
        ]
        super().__init__(placeholder="Select a report type...", options=options)

    async def callback(self, interaction: discord.Interaction):
        report_type = self.values[0]
        await interaction.response.send_message(f"You selected: {report_type}. Please attach your report file or image.", ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.attachments
        log_channel = 1323505580781867048
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            attachment = msg.attachments[0]
            await interaction.followup.send(f"Reported {report_type} with attachment: {attachment.url}", ephemeral=True)

            embed = discord.Embed(
                title="New Report",
                description=f"Reported **{report_type}** by **{interaction.user.mention}**",
                color=discord.Color.from_str("#ffb4f1")
            )
            embed.set_image(url=attachment.url)
            embed.set_thumbnail(url=interaction.user.avatar._url)
            embed.set_footer(text= time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            channel = interaction.client.get_channel(log_channel)
            await channel.send(embed=embed)
        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't provide an attachment in time.", ephemeral=True)


class ReportView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ReportDropDown())  # Add the dropdown to the view

class Essence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="reports")
    async def reports(self, ctx: commands.Context):
        view = ReportView()  # Create the view that includes the dropdown
        await ctx.send("Select a report type:", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Essence(bot))