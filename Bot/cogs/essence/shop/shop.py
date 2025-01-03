import discord
from discord.ext import commands
from .shop_setup import MainShopView
from config import Bot

class Shop(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = bot.database
        self.collection = self.db["user_data"]
        self.bbs_emojis = "<:Berrybush_Seeds:1322750639557709926>"


    @commands.hybrid_command(name="shops")
    async def shops(self, ctx: commands.Context):

        bbs = self.collection.find_one({"_id": str(ctx.author.id)})["bbs"]

        embed = discord.Embed(
            title= "Ark Essence Shop",
            description= "",
            color= discord.Color.from_str("#ffb4f1")
        )
        embed.set_thumbnail(url=ctx.guild.icon._url)
        embed.set_image(url="https://media.discordapp.net/attachments/1324362312211238912/1324402269655007343/Admin_Shop.png?ex=6778053b&is=6776b3bb&hm=538345e0c2644243a912e79d39284ce359d54fedb96cdfd50f92e1440b831859&=&format=webp&quality=lossless")
        embed.add_field(name="", value=f"{self.bbs_emojis}{bbs}", inline=False)
        await ctx.send(embed=embed, view = MainShopView(database=self.db))


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
    bot.add_view(MainShopView(database=bot.database))    