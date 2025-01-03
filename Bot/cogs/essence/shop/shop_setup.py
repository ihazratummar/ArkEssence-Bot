import discord
import constants
import time



class MainShopView(discord.ui.View):
    def __init__(self, database):
        super().__init__(timeout=None)
        self.database = database
        self.add_item(MainShopSelect(database=self.database) ) # Add the dropdown to the view


class MainShopSelect(discord.ui.Select):
    def __init__(self, database):
        self.database = database
        options = [
            discord.SelectOption(label="Dinos", emoji="🦖", description="Browse dinos by size and type.", value="Dinos"),
            discord.SelectOption(label="Tools", emoji="⛏️", description="Check out useful tools.", value="Tools"),
            discord.SelectOption(label="Weapons", emoji="⚔️", description="Browse primitive weapons.", value="Weapons"),
            discord.SelectOption(label="Armor", emoji="🛡️", description="Find armor sets.", value="Armor"),
            discord.SelectOption(label="Ammo", emoji="💥", description="Shop for ammo.", value="Ammo"),
            discord.SelectOption(label="Skins", emoji="🎨", description="Get custom skins.", value="Skins"),
            discord.SelectOption(label="Chibis", emoji="✨", description="Cute Chibi creatures.", value="Chibis"),
            discord.SelectOption(label="Admin Services", emoji="👑", description="Special requests and services.", value="Admin Services"),
        ]
        super().__init__(placeholder="Select a category...", options=options, custom_id="main_shop_select", row=0)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0] if self.values else None

        if category == "Dinos":
           await self.update_view_with_buttons(interaction, "🦖 **Dinos Menu**")
        elif category == "Tools":
            tools_item = [
                ("Chain Saw(Journeyman Only)", 400),
                ("Mining Drill(Journeyman Only)", 500),
                ("Climbing Pick", 400)
            ]
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(tools_item, f"Select a tool", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(view=self.view)

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
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(weapons, f"Select a weapon", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(view=self.view)

        elif category == "Armor":
        
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
            await interaction.response.edit_message(view=self.view)

        elif category == "Chibis":
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

            dropdown = ItemDropDown(chibis, f"Select a Chibis", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(view=self.view)

        elif category == "Skins":
            skins = [
                ("Single Skin", 200),
                ("Set of Armor Skins", 400)
            ]
            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(skins, f"Select Skin", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(view=self.view)

        elif category == "Admin Services":
            admin_services = [
                ("Admin Paint Job", 200),
            ]

            self.view.clear_items()
            self.view.add_item(self)

            dropdown = ItemDropDown(admin_services, f"Select a admin service", self.database)
            self.view.add_item(dropdown)
            await interaction.response.edit_message(view=self.view)

        elif category == "Ammo":
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
            await interaction.response.edit_message(view=self.view)
        else:
            await interaction.response.send_message("This category is under construction!", ephemeral=True)

    async def update_view_with_buttons(self, interaction: discord.Interaction, menu_title: str):
        self.view.clear_items()
        self.view.add_item(self)  # Re-add the dropdown to row 0

        # Add buttons dynamically
        buttons = [
            ("Small Dinos", "🦎"),
            ("Medium Dinos", "🦕"),
            ("Utility Dinos", "🐘"),
            ("Large Dinos", "🦏"),
            ("Rare Dinos", "🔥"),
        ]
        for label, emoji in buttons:
            button = discord.ui.Button(label=f"{label}", style=discord.ButtonStyle.primary, emoji=emoji, row=1)
            button.callback = self.create_dino_callback(label)
            self.view.add_item(button)

        self.view.add_item(BackToMainMenuButton(database=self.database))
        await interaction.response.edit_message(content=menu_title, view=self.view)

    def create_dino_callback(self, dino_type: str):
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
                dropdown = ItemDropDown(chunk, f"Select a {dino_type}", self.database)
                self.view.add_item(dropdown)

            await interaction.response.edit_message(content=f"**Select a {dino_type}:**", view=self.view)

        return callback




class ItemDropDown(discord.ui.Select):
    def __init__(self, items: list[tuple[str, int]], placeholder: str, database):
        self.items = items
        self.database = database
        self.collection = self.database["user_data"]
        
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

        modal = QuantityModal(dino_type=selected_item, price= selected_item_price , database= self.database)

        await interaction.response.send_modal(modal)





class BackToMainMenuButton(discord.ui.Button):
    def __init__(self, database):
        self.database = database
        super().__init__(label="Back to Main Menu", style=discord.ButtonStyle.secondary, emoji="🔙")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Back to Main Menu", view=MainShopView(database=self.database))


class QuantityModal(discord.ui.Modal, title = "Quantity Selection"):
    item_name: str
    price: int
    quantity = discord.ui.TextInput(label="Quantity", placeholder="Enter quantity (e.., 1)", required=True, default=1)


    def __init__(self, dino_type: str, price: int, database, isAmmo: bool = False):
        super().__init__()
        self.item_name = dino_type
        self.price = price
        self.db = database
        self.collection = self.db["user_data"]

    async def on_submit(self, interaction: discord.Interaction):
        try:
            qty = int(self.quantity.value)
            if qty < 1 :
                raise ValueError("Quantity must be at least 1")
            
            user_bbs = self.collection.find_one({"_id": str(interaction.user.id)})["bbs"]
            total_price = qty * self.price
            if user_bbs < total_price:
                await interaction.response.send_message(f"Insufficient BBS. You need {total_price} Bushberries  to buy {qty} {self.item_name}", ephemeral=True)
                return
            self.collection.update_one({"_id": str(interaction.user.id)}, {"$inc": {"bbs": -total_price}})

            embed = discord.Embed(
                title= "Purchase Successful",
                description= f"Thank you {interaction.user.mention} for buying {qty} {self.item_name} for {constants._Emojis.bbs}{total_price} Bushberries ",
                color= discord.Color.from_str("#ffb4f1")
            )
            embed.set_footer(text= time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
             # Correcting the roles fetching
            ping_roles_list = [constants._Roles.owner, constants._Roles.head_admin, constants._Roles.admin]
            mentions = []

            for role_id in ping_roles_list:
                role = interaction.guild.get_role(role_id)  # Fetch each role by ID
                if role:
                    mentions.append(role.mention)  # Add role mention if found

            # Send the message with the role mentions
            if mentions:
                await interaction.response.send_message(f"{' '.join(mentions)}", embed=embed)
            else:
                await interaction.response.send_message(embed=embed)  # Fallback if no roles found

            await interaction.followup.send(f"{interaction.user.mention} has bought {qty} {self.item_name} for {constants._Emojis.bbs}{total_price} Bushberries ")
        except ValueError as e:
            await interaction.response.send_message(f"Invalid quantity: {e}", ephemeral=True)
