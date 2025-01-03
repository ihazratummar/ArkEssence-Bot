from time import sleep

import discord
import constants
import time
from core import embeds



class MainShopView(discord.ui.View):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database
        self.add_item(MainShopSelect(database=self.database) ) # Add the dropdown to the view


class MainShopSelect(discord.ui.Select):
    def __init__(self, database):
        self.database = database
        self.collection = self.database["user_data"]
        options = [
            discord.SelectOption(label="Dinos", emoji="🦖", description="Browse dinos by size and type.", value="Dinos"),
            discord.SelectOption(label="Tools", emoji=constants._Emojis.tools, description="Check out useful tools.", value="Tools"),
            discord.SelectOption(label="Weapons", emoji = constants._Emojis.weapon, description="Browse primitive weapons.", value="Weapons"),
            discord.SelectOption(label="Armor", emoji= constants._Emojis.armor, description="Find armor sets.", value="Armor"),
            discord.SelectOption(label="Ammo", emoji= constants._Emojis.ammo, description="Shop for ammo.", value="Ammo"),
            discord.SelectOption(label="Skins", emoji= constants._Emojis.skin, description="Get custom skins.", value="Skins"),
            discord.SelectOption(label="Chibis", emoji= constants._Emojis.chibis, description="Cute Chibi creatures.", value="Chibis"),
            discord.SelectOption(label="Admin Services", emoji= constants._Emojis.admin_service, description="Special requests and services.", value="Admin Services"),
        ]
        super().__init__(placeholder="Select a category...", options=options, custom_id="main_shop_select", row=0)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0] if self.values else None
        bbs = self.collection.find_one({"_id": str(interaction.user.id)})["bbs"]
        
        if category == "Dinos":
            embed = embeds.shop_embed(
                image="https://media.discordapp.net/attachments/1013016741984608280/1318804034332655676/Dino_Showcase.png?ex=6778bf77&is=67776df7&hm=017e210cc4485bdf6c8a3c280139e8ee3f82260ec8975a6dff447d21d158160b&=&format=webp&quality=lossless&width=550&height=183",
                thumbnail= interaction.guild.icon._url,
                bbs= bbs)
            await self.update_view_with_buttons(interaction= interaction, embed=embed, bbs = bbs)
        elif category == "Tools":

            embed = embeds.shop_embed(
                image= "https://media.discordapp.net/attachments/1013016741984608280/1324234135145025587/Tools.png?ex=6778ba24&is=677768a4&hm=cc484b13aabad02308b2e869f67dca27627fcd417136ec02ce558e0f433a0a5e&=&format=webp&quality=lossless",
                thumbnail= interaction.guild.icon._url,
                bbs=bbs
            )

            tools_item = [
                ("Chain Saw(Journeyman Only)", 400),
                ("Mining Drill(Journeyman Only)", 500),
                ("Climbing Pick", 400)
            ]
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(tools_item, f"Select a tool", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed, view=self.view)

        elif category == "Weapons":
            weapons = [
                    ("Flamethrower", 400),
                    ("Long Neck Rifle", 600),
                    ("Assault Rifle", 400),
                    ("Simple Pistol", 100),
                    ("Shotgun", 400),
                    ("Pump Action Shotgun", 500),
                    ("Rocket Launcher", 500),
                    ("Harpoon", 400),
                    ("Fabricated Sniper", 500),
                    ("Fabricated Pistol", 400),
                    ("Minigun", 600),
                    ("Cruise Missile", 700),
                    ("Crossbow", 400),
                    ("Compound Bow", 500),
                    ("Tek Railgun", 700),
                    ("Tek Sword", 700),
                    ("Tek Claws", 700),
                    ("Tek Rifle", 700),
                    ("Tek Grenade Launcher", 800),
                ]
            
            embed = embeds.shop_embed(
                image= "https://media.discordapp.net/attachments/1013016741984608280/1324235021887864874/Weapons.png?ex=6778baf8&is=67776978&hm=2dd25d3fec19895a0ad3503aa0752cb4fccb1f5074d747abc29374a60a22573f&=&format=webp&quality=lossless",
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(weapons, f"Select a weapon", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed , view=self.view)

        elif category == "Armor":
            embed = embeds.shop_embed(
                image= "https://media.discordapp.net/attachments/1013016741984608280/1324235933511581809/Weapons_1.png?ex=6778bbd1&is=67776a51&hm=d85082dc2abe9a5c2fe889339fae0396af243ba2edf8abe2943958213fc4f40d&=&format=webp&quality=lossless",
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            armor_sets = [
                ("Ascendant Hide Set", 200),
                ("Ascendant Fur Set", 300),
                ("Ascendant Desert Gear", 300),
                ("Ascendant Ghillie Set", 400),
                ("Ascendant Chitin Set", 500),
                ("Ascendant Flak Gear", 800),
                ("Ascendant Hazard Set", 800),
                ("Ascendant Scuba Gear", 800),
                ("Ascendant Riot Gear", 900),
                ("Tek Suit", 1000),
            ]

            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(armor_sets, f"Select a Ammo", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed, view=self.view)

        elif category == "Chibis":
            embed = embeds.shop_embed(
                image= "https://media.discordapp.net/attachments/1013016741984608280/1324233364898840647/Chibis.png?ex=6778b96d&is=677767ed&hm=ed826ee95648ada9cc45e0e5e4f65bc689ce623cf96c0f562c51a08e8870d8b2&=&format=webp&quality=lossless",
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            chibis = [
                ("Common Chibis (Green)", 300),
                ("Uncommon Chibis (Blue)", 400),
                ("Rare Chibis (Purple)", 500),
                ("Very Rare Chibis (Yellow)", 600),
                ("Legendary Chibis (Red)", 800),
                ("Mystery Chibi Pack (1 From Each Tier + 2 Extra)", 900),
            ]
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(chibis, f"Select a Chibis", self.database, isChibi= True)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed, view=self.view)

        elif category == "Skins":
            embed = embeds.shop_embed(
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            skins = [
                ("Single Skin", 200),
                ("Set of Armor Skins", 400)
            ]
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(skins, f"Select Skin", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed, view=self.view)

        elif category == "Admin Services":
            embed = embeds.shop_embed(
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            admin_services = [
                ("Admin Paint Job", 200),
            ]

            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(admin_services, f"Select a admin service", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed , view=self.view)

        elif category == "Ammo":
            embed = embeds.shop_embed(
                image= "https://media.discordapp.net/attachments/1013016741984608280/1324237087595036693/Weapons_2.png?ex=6778bce4&is=67776b64&hm=86c32210b2adc919bc147705a227aecf11832224dce925f9a1700be9b47ef571&=&format=webp&quality=lossless",
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )
            ammo_list = [
                ("Flame Arrows", 1.5),
                ("Simple Shotgun Ammo", 1.5),
                ("Advanced Bullet", 1.5),
                ("Advanced Rifle Bullet", 1.5),
                ("Advanced Sniper Bullet", 1.5),
                ("Shocking Tranq", 1.5),
                ("Flamethrower Ammo", 1.5),
                ("Chain Bola", 1.5),
                ("Grappling Hook", 1.5),
                ("Net Projectile", 1.5)
            ]

            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(ammo_list, f"Select a admin service", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(embed= embed, view=self.view)
        else:
            await interaction.response.send_message("This category is under construction!", ephemeral=True)

    async def update_view_with_buttons(self, interaction: discord.Interaction, embed: discord.Embed, bbs):
        self.view.clear_items()
        self.view.add_item(self)  # Re-add the dropdown to row 0

        # Add buttons dynamically
        buttons = [
            ("Small Dinos", constants._Emojis.small_dino),
            ("Medium Dinos", constants._Emojis.medium_dino),
            ("Utility Dinos", constants._Emojis.utility_dino),
            ("Large Dinos", constants._Emojis.large_dino),
            ("Rare Dinos", constants._Emojis.rare_dino),
        ]
        for label, emoji in buttons:
            button = discord.ui.Button(label=f"{label}", style=discord.ButtonStyle.primary, emoji=emoji, row=1)
            button.callback = self.create_dino_callback(label, bbs)
            self.view.add_item(button)

        # self.view.add_item(BackToMainMenuButton(database=self.database, embed=embed))
        await interaction.response.edit_message( embed= embed,  view=self.view)

    def create_dino_callback(self, dino_type: str, bbs):
        async def callback(interaction: discord.Interaction):
            dinos = {
            "Small Dinos": (["Achatina", "Dilo", "Diplocaulus", "Dung Beetle", "Dodo", "Keriku", "Lystro", "Moschops", "Pachy", "Pego", "Phioma", "Pteranodon","Troodon" ], 400),
            "Medium Dinos": ([
                "Areno", "Arthro", "Baryonyx", "Basilosaurus", "Carbonemys", "Carno", 
                "Chalicotherium", "Dimetrodon", "Direwolf", "Dunkleo", "Eel", "Equus", 
                "Galli", "Hyaenodon", "Iguanodon", "Kapro", "Kentro", "Leonis", 
                "Lymantria", "Manta", "Megaloceros", "Megalodon", "Megatherium", 
                "Morellatops", "Parasaur", "Pachyrhinosaur", "Pelagornis", 
                "Procoptodon", "Purlovia", "Raptor", "Ravenger", "Rollrat", 
                "Sabertooth", "Tapejara", "Thyla", "Tigris", "Titanoboa", "Trike", 
                "Wooly Rhino"], 500),
            "Utility Dinos": ([
                "Angler", "Ankylo", "Argentavis", "Beaver", "Beelzebufo", "Bronto", 
                "Daeodon", "Direbear", "Doedi", "Gacha", "Giant Bee", "Maewing", 
                "Mammoth", "Mantis", "Ovis", "Snow Owl", "Therizino"
                ], 600),
            "Large Dinos": ([
                "Allo", "Ancient Zaldrir Dragon", "Basilisk", "Giga", "Gigantoraptor", 
                "Gryphon", "Karkinos", "Mana", "Megalosaurus", "Mosa", 
                "Paracer", "Plesiosaur", "Rex", "RockDrake", "Spino", 
                "Tusoteuthis", "Velo", "(Amissa) Wyvern (Specify type)", "Yuty"
                ], 900),
            "Rare Dinos": ([
                "Phoenix", "Reaper (Male Only)", "Rock Elementals"
                ], 1000)
        }
            
            dino_images = {
            "Small Dinos": "https://media.discordapp.net/attachments/1013016741984608280/1324216583652118599/Small_Dinos.png?ex=6778a9cc&is=6777584c&hm=852bfbd1afaddf1da12fc0dba3041f7888568583881351ab4934eab450bfbb17&=&format=webp&quality=lossless",
            "Medium Dinos": "https://media.discordapp.net/attachments/1013016741984608280/1324222698838032404/Medium.png?ex=6778af7e&is=67775dfe&hm=014b53d1f0c68578d3bb3881a11bc9dfa507d024fbc9e6779460135ddbc1ecb7&=&format=webp&quality=lossless",
            "Utility Dinos": "https://media.discordapp.net/attachments/1013016741984608280/1324223345172156447/Utility.png?ex=6778b018&is=67775e98&hm=122eebf2845f8c0f66ca23bdadd87177a295858a0fc082d9dad58b321831709d&=&format=webp&quality=lossless",
            "Large Dinos": "https://media.discordapp.net/attachments/1013016741984608280/1324225538272788492/Large_1.png?ex=6778b223&is=677760a3&hm=87a6d0074b543afc39d9fe5fae5519dd197ed51eaba8ab41a2e36097ab0c2fca&=&format=webp&quality=lossless",
            "Rare Dinos": "https://media.discordapp.net/attachments/1013016741984608280/1324231550031761429/Unbreedable.png?ex=6778b7bc&is=6777663c&hm=d83c53f91b4255ba2b23817965a71b9a722123d43add454cfc0b48acd66e5fff&=&format=webp&quality=lossless"
        }
            
            dino_items, price = dinos[dino_type]
            items_with_price = list(zip(dino_items, [price] * len(dino_items)))

            # Clear previous items from row 2 (remove previous dropdown if exists)
            for item in self.view.children:
                if isinstance(item, ItemDropDown):
                    self.view.remove_item(item)
            # Add the dropdown for dinos in row 2
            dropdown_chunks = [
            items_with_price[i:i + 25] for i in range(0, len(items_with_price), 25)
             ]

            for chunk in dropdown_chunks:
                dropdown = ItemDropDown(chunk, f"Select a {dino_type}", self.database, isDino= True )
                self.view.add_item(dropdown)
            selected_image = dino_images.get(dino_type, "")
            embed = embeds.shop_embed(
                image=selected_image,
                thumbnail= interaction.guild.icon._url,
                bbs= bbs
            )

            await interaction.response.edit_message(embed= embed ,  view=self.view)

        return callback




class ItemDropDown(discord.ui.Select):
    def __init__(self, items: list[tuple[str, int]], placeholder: str, database, isChibi: bool = False, isDino: bool  =False):
        self.items = items
        self.database = database
        self.collection = self.database["user_data"]
        self.isChibi = isChibi
        self.isDino = isDino
        
        truncated_items = items[:25]
        options = [
            discord.SelectOption(
                label=item_name, description=f"Price: {item_price}"
            )
            for item_name, item_price in truncated_items
        ]

        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_item = self.values[0]
        selected_item_price = next(price for item_name, price in self.items if item_name == selected_item)

        modal = QuantityModal(dino_type=selected_item, price= selected_item_price , database= self.database, isChibi=self.isChibi, isDino= self.isDino)

        await interaction.response.send_modal(modal)





class BackToMainMenuButton(discord.ui.Button):
    def __init__(self, database, embed):
        self.embed = embed
        self.database = database
        super().__init__(label="Back to Main Menu", style=discord.ButtonStyle.secondary, emoji="🔙")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=MainShopView(database=self.database), embed= self.embed)


class QuantityModal(discord.ui.Modal, title = "Quantity Selection"):
    item_name: str
    price: int
    quantity = discord.ui.TextInput(label="Quantity", placeholder="Enter quantity (e.., 1)", required=True, default=1)
    


    def __init__(self, dino_type: str, price: int, database, isChibi: bool = False, isDino: bool = False):
        super().__init__()
        self.item_name = dino_type
        self.price = price
        self.db = database
        self.collection = self.db["user_data"]
        self.isChibi = isChibi
        self.isDino = isDino

        if isDino:
            self.dino_gender = discord.ui.TextInput(
                label="Type Dino Gender",
                placeholder= "Enter Gender (e.g., Male, Female, Breeding Pair)",
                required= True
            )
            self.add_item(self.dino_gender)

        if isChibi:
            self.type_of_chibi = discord.ui.TextInput(label="Type of Chibi", placeholder="Enter the type of chibi", required=True)
            self.add_item(self.type_of_chibi)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            qty = int(self.quantity.value)
            if qty < 1 :
                raise ValueError("Quantity must be at least 1")

            adjusted_qty = qty  # Default adjusted quantity
            gender = None

            # Handle Dino-specific logic
            if self.isDino:
                gender = self.dino_gender.value.strip().lower()
                if gender not in {"male", "female", "breeding pair"}:
                    raise ValueError("Invalid gender. Must be 'Male', 'Female', or 'Breeding Pair'.")
                if gender == "breeding pair":
                    adjusted_qty *= 2  # Double the quantity for breeding pairs


            user_bbs = self.collection.find_one({"_id": str(interaction.user.id)})["bbs"]
            total_price = adjusted_qty * self.price

            # Apply breeding pair price adjustment
            if self.isDino and gender == "breeding pair":
                total_price = int(total_price * 1.2)  # 20% increase

            if user_bbs < total_price:
                await interaction.response.send_message(f"Insufficient BBS. You need {constants._Emojis.bbs}{total_price} to buy {qty} {self.item_name}", ephemeral=True)
                return


            embed = discord.Embed(
                title= "Purchase Successful",
                description= f"Thank you {interaction.user.mention} for shopping here at Ark Essence, Please pick up your items at the Community Center in your vault",
                color= discord.Color.from_str("#ffb4f1")
            )
            embed.add_field(name="Item", value= self.item_name, inline= True)
            if self.isDino:
                embed.add_field(name="Gender", value= self.dino_gender)
            embed.add_field(name="", value="", inline=False)
            if self.isDino:
                if gender == "breeding pair":
                    embed.add_field(name="Quantity", value=f"{adjusted_qty}({int(adjusted_qty/2)} Male, {int(adjusted_qty/2)} Female )", inline=True)
                else:
                    embed.add_field(name="Quantity", value=adjusted_qty, inline=True)
            else:
                embed.add_field(name= "Quantity", value= adjusted_qty, inline= True)
            embed.add_field(name= "Total Price", value= f"{constants._Emojis.bbs}{total_price}", inline= True)
            if self.isChibi:
                embed.add_field(name= "Chibi Type", value= self.type_of_chibi.value)



            embed.set_footer(text= time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
             # Correcting the roles fetching
            ping_roles_list = [constants._Roles.owner, constants._Roles.head_admin, constants._Roles.admin]
            mentions = []

            for role_id in ping_roles_list:
                role = interaction.guild.get_role(role_id)  # Fetch each role by ID
                if role:
                    mentions.append(role.mention)  # Add role mention if found
            logger_channel = interaction.guild.get_channel(constants._Channels.shop_order_log)
            # Send the message with the role mentions

            if self.isDino:
                paint = DinoPaintJob(total_price= total_price, quantity= adjusted_qty, collection= self.collection, mention=mentions, log_channel=logger_channel, embed=embed)
                await interaction.response.send_message(embed=embed, view=paint)
            else:
                self.collection.update_one({"_id": str(interaction.user.id)}, {"$inc": {"bbs": - total_price}})

                if mentions:
                    await logger_channel.send( f"{' '.join(mentions)}",embed=embed)
                else:
                    await interaction.response.send_message(embed=embed)  # Fallback if no roles found

                await interaction.response.send_message(embed = embed)
        except ValueError as e:
            await interaction.response.send_message(f"Invalid quantity: {e}", ephemeral=True)


class DinoPaintJob(discord.ui.View):
    def __init__(self, total_price, quantity, collection, mention , log_channel, embed):
        self.total_price = total_price
        self.quantity =  quantity
        self.collection = collection
        self.mention = mention
        self.log_channel = log_channel
        self.embed =embed

        super().__init__(timeout=None)
    @discord.ui.button(label="Apply Paint")
    async def apply_paint(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(content="Applied Paint", view= self)

    @discord.ui.button(label="Complete Purchase")
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.collection.update_one({"_id": str(interaction.user.id)}, {"$inc": {"bbs": -self.total_price}})
        button.disabled = True
        if self.mention:
            await self.log_channel.send(f"{' '.join(self.mention)}", embed=self.embed)

        await interaction.response.edit_message(embed=self.embed, view= self)