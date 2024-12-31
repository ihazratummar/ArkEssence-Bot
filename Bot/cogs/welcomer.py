import discord
from discord.ext import commands





class Welcomer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return


        channel_id = 1322481571995062332
        channel = member.guild.get_channel(channel_id)

        embed = discord.Embed(
            title="︵‿୨♡Welcome To Ark Essence♡୧‿︵",
            description="""This is a PVE Ark Survival Ascended Server for Xbox and Microsoft PC players. Our server is password-protected, and the password can be found after verifying and visiting the Server Info channel. 
            \n <:pinkbullet:1104598763395354746>Please note that this server is for players 16 and older.""",
            color=discord.Color.from_str("#ffb4f1")  # Replace with your desired hex color
        )
        embed.add_field(name="To join, follow these steps:", value="", inline=False)
        embed.add_field(name="", value="<:1868white1:1033953506710790275> Read the Rules to verify and unlock access to the rest of the Discord server.", inline=False)
        embed.add_field(name="", value="<:7366white2:1033954027840487454> React to the Self Roles channel to customize your roles.", inline=False)
        embed.add_field(name="", value="<:5656white3:1033953509680357476> React to the Ark Roles channel for Ark-specific roles.", inline=False)
        embed.add_field(name="", value="<:6136white4:1033953512633151578> Visit the Server Info channel to find the server password and details to join.\n", inline=False)
        embed.add_field(name="", value="If you have any questions, feel free to open a ticket, and one of our staff members will assist you.\n", inline=False)
        embed.add_field(name="", value="Happy gaming,\nArk Essence Staff", inline=False)
        embed.set_thumbnail(url=member.avatar._url)
        embed.set_image(url="https://media.discordapp.net/attachments/1013016741984608280/1323105720178053212/Ark_Essence_4.gif?ex=67734db9&is=6771fc39&hm=175b534f3daf4d5f6413c3cffaaf58db28dff750e2225f7bba5c9d7c42c4c658&=&width=550&height=183")

        if channel is None:
            return
        await channel.send(embed=embed)




async def setup(bot: commands.Bot):
    await bot.add_cog(Welcomer(bot))