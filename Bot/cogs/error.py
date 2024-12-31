import discord
from discord.ext import commands
from discord import app_commands
from config import Bot


class ErrorCog(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error


    async def on_app_command_error(
            self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingAnyRole):
            role = interaction.guild.get_role(error.missing_roles)
            await interaction.response.send_message(f"Missing role error: {role.name}", ephemeral = True)
        
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                f"Missing permissions Error: {error}", ephemeral=True
            )

        elif isinstance(error, app_commands.CommandOnCooldown):
            retry_after = round(error.retry_after)
            await interaction.response.send_message(
                f"Command OnCooldown Error. Try again after {retry_after} seconds.", ephemeral=True
            )


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.Command):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"Command not found")
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Incorrect arguments entered")

        elif isinstance(error, commands.MissingPermissions):
            perms = ", ".join(error.missing_permissions)
            return await ctx.send(f"You need {perms} to use this command.")
        
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Command on cooldown. Try again later.")

        elif isinstance(error, commands.ConversionError):
            return await ctx.send("Invalid arguments provided.")

        elif isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"Member not found.")

        else:
            # Logging the error or handling it in some way before re-raising
            print(f"Unhandled error: {error}")
            raise error
        
async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorCog(bot))