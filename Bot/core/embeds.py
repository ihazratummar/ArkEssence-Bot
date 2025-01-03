import discord
import constants



def shop_embed(
        title: str = "Ark Essence Shop",
        description: str = "",
        color: discord.Color = discord.Color.from_str("#ffb4f1"),
        image: str = "https://media.discordapp.net/attachments/1324362312211238912/1324402269655007343/Admin_Shop.png?ex=6778053b&is=6776b3bb&hm=538345e0c2644243a912e79d39284ce359d54fedb96cdfd50f92e1440b831859&=&format=webp&quality=lossless",
        fields: list = None,
        footer: str = None,
        thumbnail: str = None,
        bbs: str = None
) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)


    embed.set_thumbnail(url= thumbnail)

    if image:
        embed.set_image(url=image)

    if fields is None:
        fields = []
    
    if bbs is not None:
        fields.insert(0, ("", f"{constants._Emojis.bbs}{bbs}", False))

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    if footer:
        embed.set_footer(text=footer)

    return embed
    
