import discord
import asyncio
import time
from discord.ui import Modal, TextInput

class ReportDropDown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Game Issue", value="Game Issue "),
            discord.SelectOption(label="Player Issue", value="Player Issue"),
        ]
        super().__init__(placeholder="Select a report type...", options=options, custom_id="report_dropdown")

    async def callback(self, interaction: discord.Interaction):
        report_type = self.values[0]
        await interaction.response.send_message(
            f"You selected: {report_type}. Please provide a description of the issue.",
            ephemeral=True,
        )

        def text_check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        def attachment_check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.attachments

        log_channel = 1323505580781867048

        try:
            # Wait for the user to provide a text description
            text_msg = await interaction.client.wait_for("message", check=text_check, timeout=60)
            description = text_msg.content

            await interaction.followup.send("Now, please attach your report file or image.", ephemeral=True)

            # Wait for the user to attach a file or image
            attach_msg = await interaction.client.wait_for("message", check=attachment_check, timeout=60)
            attachment = attach_msg.attachments[0]

            # Send confirmation to the user
            await interaction.followup.send(
                f"Reported {report_type} with description and attachment: {attachment.url}",
                ephemeral=True,
            )

            # Send the report to the log channel
            embed = discord.Embed(
                title="New Report",
                description=f"**Type:** {report_type}\n**Description:** {description}\n**Reported by:** {interaction.user.mention}",
                color=discord.Color.from_str("#ffb4f1"),
            )
            embed.set_image(url=attachment.url)
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_footer(text=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
            channel = interaction.client.get_channel(log_channel)
            await channel.send(embed=embed)

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't provide the required information in time.", ephemeral=True)



class ReportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ReportDropDown())  # Add the dropdown to the view