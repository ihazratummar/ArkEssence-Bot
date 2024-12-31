import discord
from github import Github 
import os
import time
from dotenv import load_dotenv
import chat_exporter

load_dotenv()

async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    
    log_channel = guild.get_channel(1015776086606487645)
    
    t = time.localtime()
    formatted_time = time.strftime("%y-%m-%d %H:%M:%S", t)
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    embed.add_field(name="Time", value=formatted_time)
    await log_channel.send(embed=embed)

async def get_transcript(member: discord.Member, channel: discord.TextChannel):
    export = await chat_exporter.export(channel = channel)
    file_name = f'{member.id}.html'
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(export)

git_token = os.getenv("GITHUB_TOKEN")
github = Github(git_token)
def upload(file_path: str, member_name: str):

    try:
        user = github.get_user()
        print(f"Authenticated as: {user.login}")
        repo = github.get_repo("ihazratummar/ArkEssenceTranscript")
        print(f"Repo: {repo.full_name}")
        file_name = f"{int(time.time())}"

        repo.create_file(
            path= f"tickets/{file_name}.html",
            message="Ticket Log {0}".format(member_name),
            branch="main",
            content=open(f"{file_path}","r",encoding="utf-8").read()
        )
        os.remove(file_path)

        return file_name
    except Exception as e:
        print(e)
        return None
