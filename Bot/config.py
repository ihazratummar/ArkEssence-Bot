import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")


uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.9fhei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri)
database = mongo_client["Economy"]


exts = {
    "cogs.rewards.economy",
    "cogs.error",
    "cogs.welcomer",
    "cogs.ticket.ticket",
    "cogs.essence.report.report",
    "cogs.essence.requests.requests",
    "cogs.essence.shop.shop",
}

class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, database, **kwargs):
        super().__init__(command_prefix, intents = intents, **kwargs)
        self.mongo_cleint = mongo_client
        self.database = database

    async def on_ready(self):
        for ext in exts:
            if ext not in self.extensions:
                await self.load_extension(ext)
        print("loaded all cogs")

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Bot is ready.")

        await self.change_presence(
            activity= discord.Game(name= "Playing Ark")
        )



if __name__ == "__main__":
    bot = Bot(command_prefix="!", intents=discord.Intents.all(), database = database, help_command=None )
    bot.run(bot_token)