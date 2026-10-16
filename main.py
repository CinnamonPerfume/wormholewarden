import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import constants

test_guild_id = constants.TEST_GUILD_ID

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()

logging = True

user_id = 0
operator_id = constants.OPERATOR_ID

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is up and running!")

@bot.command(description="Ping!")
async def ping(interaction: nextcord.Interaction):
    if interaction.user.id != operator_id:
        await interaction.response.send_message("You don't have the permissions to run this command.", ephemeral=True)
    await interaction.channel.send(f"Pong")
    await interaction.channel.send(f"Bot is active.")

@bot.slash_command(description="List of servers the bot is in")
async def guild_list(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"Retrieving a list of all guilds with Wormhole Warden...")
    for guild in bot.guilds:
        await interaction.channel.send(f"{guild.name}")

@bot.slash_command(description="Ban user from all servers the bot is in.")
async def global_ban(interaction: nextcord.Interaction, reason: str):
    if not interaction.user.guild_permissions.administrator and interaction.user.id != operator_id:
        await interaction.response.send_message("You don't have the permissions to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Banning...")
        for guild in bot.guilds:
            try:
                user = await bot.fetch_user(user_id)
                await guild.ban(user, reason=reason)
                await interaction.channel.send(f"Banned {user.mention} from {guild.name}")
            except nextcord.NotFound:
                await interaction.response.send_message(f"User with ID {user_id} not found.")
            except nextcord.Forbidden:
                await interaction.response.send_message(f"Missing permissions to ban user {user_id} in {guild.name}.")
            except Exception as e:
                await interaction.response.send_message(f"An error occured: {e}")
        if logging:
            log_channel = bot.get_channel(constants.LOGSCHANNEL)
            await log_channel.send(f"{user.mention} **(Username: {user.name})** was banned globally from all servers by <@{operator_id}>. \nReason: {reason}")
        else:
            print("Logs channel not found or bot doesn't have access.")

@bot.slash_command(description="Unban user from all servers the bot is in.")
async def global_unban(interaction: nextcord.Interaction, reason: str):
    if not interaction.user.guild_permissions.administrator and interaction.user.id != operator_id:
        await interaction.response.send_message("You don't have the permissions to run this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Unbanning...")
        for guild in bot.guilds:
            try:
                user = await bot.fetch_user(user_id)
                await guild.unban(user, reason=reason)
                await interaction.channel.send(f"Unbanned {user.mention} from {guild.name}")
            except nextcord.NotFound:
                await interaction.response.send_message(f"User with ID {user_id} not found.")
            except nextcord.Forbidden:
                await interaction.response.send_message(f"Missing permissions to unban user {user_id} in {guild.name}.")
            except Exception as e:
                await interaction.response.send_message(f"An error occured: {e}")
        if logging:
            log_channel = bot.get_channel(constants.LOGSCHANNEL)
            await log_channel.send(f"{user.mention} **(Username: {user.name})** has been unbanned globally from all servers by <@{operator_id}>. \nReason: {reason}")
        else:
            print("Logs channel not found or bot doesn't have access.")

bot.run(constants.TOKEN)