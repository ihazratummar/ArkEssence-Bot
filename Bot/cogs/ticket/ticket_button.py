import discord
from discord.ui import View, button, Button
import asyncio
from cogs.ticket import helper_function




class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Create Ticket", style=discord.ButtonStyle.blurple, emoji="<:ticket_pink:1323149085599072356>", custom_id="ticketopen")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)   


        category : discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1014183152786341950)
        for ch in category.text_channels:
            if ch.topic ==f"{interaction.user.id} DO NOT CHNAGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send("You are already have a ticket in {0}".format(ch.mention), ephemeral= True)
                return
        
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages = False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = True),
            interaction.guild.me :  discord.PermissionOverwrite(read_messages = True, send_messages = True)
        }

        channel = await category.create_text_channel(
            name=f"ticket-{interaction.user}",
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            reason="Ticket Created",
            overwrites = overwrites
        )


        embed= discord.Embed(
                title="︵‿୨♡୧‿︵ 𓆩♡𓆪 ︵‿୨♡୧‿︵*Report Ticket*︵‿୨♡୧‿︵ 𓆩♡𓆪 ︵‿୨♡୧‿︵",
                description="""*When submitting a report, please ensure you provide detailed information along with relevant images or clips of the incident.*\n\n
                For in-game reports involving player behavior, include clear evidence.\n\n
                For harassment on Discord, submit your report here.\n\n
                This is also to report any game bugs or server issues\n\n
                Name:
                Tribe:
                Issue:
                When:\n\n
                Thank you for helping us maintain a safe and welcoming community!""",
                color=discord.Color.from_str("#ffb4f1")  # Replace with your desired hex color
            )
        embed.set_author(name="Ark Essence Staff", icon_url=interaction.guild.icon._url)
        embed.set_image(url="https://media.discordapp.net/attachments/1013016741984608280/1318805072175431760/Tickets.png?ex=6772d1af&is=6771802f&hm=5f624332f7664c6dafbb461994b97db4ea6e08ea45ff32fb277415b4e155dde3&=&format=webp&quality=lossless")
        await channel.send(embed=embed, view=TicketCloseButton()),
        await interaction.followup.send( 
            embed= discord.Embed(
                    description = "Created your ticket in {0}".format(channel.mention),
                    color = discord.Color.blurple()), 
                    ephemeral=True
                    )
        await helper_function.send_log(
            title="Ticket Created",
            description="**Created by** {0}".format(interaction.user.mention),
            color= discord.Color.green(),
            guild= interaction.guild
        )
        




class TicketCloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Thank You For Reporting", style=discord.ButtonStyle.red, emoji="🔒", custom_id="ticketclose")
    async def close_ticketasync (self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        
        await interaction.channel.send("This ticket will be closed in 5 seconds")
        await asyncio.sleep(5)

        closed_category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1015794218582683730)

        if closed_category is None:
            await interaction.channel.send("Could not find the closed tickets category. Please contact an admin.")
            return
        
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages = False),
            interaction.guild.me :  discord.PermissionOverwrite(read_messages = True, send_messages = True)
        }

        await interaction.channel.edit(category=closed_category, overwrites=overwrites, reason="Ticket Closed")

        allowed_role_ids = [1032140494559527004, 1013016741485477929, 1013016741485477930, 1013016741464526915]

        await interaction.channel.send(
            embed= discord.Embed(
                description="Ticket is Closed",
                color=discord.Color.red()
            ),
            view= TrushButton(allowed_role_ids=allowed_role_ids)
        )

        topic_parts = interaction.channel.topic.split(" ")
        member_id = topic_parts[0] if topic_parts else None

        print(f"Debug: parsed member_id: {member_id}")

        if member_id:
            try:
                member = await interaction.guild.fetch_member(int(member_id))
                print(f"Debug: found member: {member}")
            except(ValueError, discord.NotFound):
                member = None

                print(f"Debug: member not found")
                
            if member:
                await helper_function.get_transcript(member= member, channel= interaction.channel)
                file_name = helper_function.upload(file_path=f'{member.id}.html',member_name=member.name)
                link = f"https://ihazratummar.github.io/ArkEssenceTranscript/tickets/{file_name}"
                await helper_function.send_log(
                    title="Ticket Closed",
                    description=f"**Closed by:** {interaction.user.mention}\n[Click for Transcript]({link})",
                    color= discord.Color.yellow(),
                    guild=interaction.guild
                )
            else:
                await interaction.followup.send("Could not find the member to send the transcript to", ephemeral=True)
        else:
            await interaction.followup.send("Could not find the member to send the transcript to", ephemeral=True)
                
            
class TrushButton(View):
    def __init__(self, allowed_role_ids):
        super().__init__(timeout=None)
        self.allowed_role_ids = allowed_role_ids

    @button(label="Delete Ticket", style=discord.ButtonStyle.red, emoji="🗑️", custom_id="ticketdelete")
    async def delete_ticket(self, interaction: discord.Interaction, button: Button):
        if interaction.user.guild_permissions.administrator or any(role.id in self.allowed_role_ids for role in interaction.user.roles):
            await interaction.response.defer(ephemeral=True)
            await interaction.channel.send("This ticket will be deleted in 5 seconds")
            await asyncio.sleep(5)
            await interaction.channel.delete(reason="Ticket Deleted")
        else:
            await interaction.response.send_message("You are not allowed to delete this ticket.", ephemeral=True)

        await helper_function.send_log(
            title= "Ticket Deleted",
            description= f"**Deleted by:** {interaction.user.mention},\n**Ticket Name:** {interaction.channel.name}",
            color= discord.Color.red(),
            guild=interaction.guild
        )