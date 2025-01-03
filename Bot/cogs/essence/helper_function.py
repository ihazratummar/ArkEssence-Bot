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



class Shop_Request_Modal(discord.ui.Modal, title = "Shop Request"):

    item_name = discord.ui.TextInput(label="Item Name", placeholder="Item Name", required=True)
    quantity = discord.ui.TextInput(label="Quantity",placeholder="100", required=True)
    notes = discord.ui.TextInput(label="Additional Note",placeholder="Notes (optional)", required=False)


    async def on_submit(self, interaction):
        item_name = self.item_name.value
        quantity = self.quantity.value
        notes = self.notes.value

        if int(quantity) <= 0 : 
            await interaction.response.send_message("Quantity must be greater than 0", ephemeral=True)
            return
        
        log_channel = 1322481571995062332


        user_mention = interaction.user.mention
        await interaction.response.send_message(
            f"{user_mention}, your shop request has been submitted!\n\nItem Name: {item_name}\nQuantity: {quantity}\nNotes: {notes}",
            ephemeral=True
        )

        embed = discord.Embed(
            title="New Shop Request",
            description=f"**Item Name:** {item_name}\n**Quantity:** {quantity}\n**Requested by:** {user_mention}",
            color=discord.Color.from_str("#ffb4f1"),
        )
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)
        
        embed.set_footer(text=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), icon_url=interaction.user.avatar.url)
        channel = interaction.client.get_channel(log_channel)
        await channel.send(embed=embed)


