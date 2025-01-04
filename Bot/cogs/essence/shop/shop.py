import discord
from discord.ext import commands
from .shop_setup import MainShopView
from config import Bot
from core import embeds


class Shop(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = bot.database
        self.collection = self.db["user_data"]
        self.bbs_emojis = "<:Berrybush_Seeds:1322750639557709926>"
        


    @commands.hybrid_command(name="shops")
    async def shops(self, ctx: commands.Context):
        user_data = self.collection.find_one({"_id": str(ctx.author.id)})
        bbs = user_data["bbs"]
        vault_number = user_data.get("vault_number")
        if not vault_number:
            await ctx.send("You need to claim a vault first to access the shop. use `/claim-vault` or `a!claim-vault` to claim a vault.")
            return

        embed = embeds.shop_embed(
            image="https://media.discordapp.net/attachments/1324362312211238912/1324402269655007343/Admin_Shop.png?ex=6778053b&is=6776b3bb&hm=538345e0c2644243a912e79d39284ce359d54fedb96cdfd50f92e1440b831859&=&format=webp&quality=lossless",
            thumbnail= ctx.guild.icon._url,
            bbs= bbs
        )
        await ctx.send(embed=embed, view = MainShopView(database=self.db))


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
    bot.add_view(MainShopView(database=bot.database))    