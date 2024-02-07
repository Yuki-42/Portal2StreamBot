"""
Main file of the project.
"""

# NOTE: THIS PROJECT REQUIRES THE FOLLOWING PACKAGES TO BE INSTALLED:
# git+https://github.com/Pycord-Development/pycord
# It is not listed in the requirements.txt file because the PIP package is very outdated.

# Standard Library Imports
from os import environ

# Third Party Imports
from discord import Bot, Intents, ApplicationContext, option, Embed
from dotenv import load_dotenv as loadDotenv

# Local Imports
from internals.help import Help
from internals._logging import createLogger, SuppressedLoggerAdapter

# Load the environment variables
loadDotenv()

# Get all required environment variables
token: str = environ.get("TOKEN")
target: str = environ.get("TARGET")
port: int = int(environ.get("PORT"))
logLevel: str = environ.get("LEVEL")

# Create the loggers
logger: SuppressedLoggerAdapter = createLogger("main", logLevel)
helpLogger: SuppressedLoggerAdapter = createLogger("help", logLevel)

# Create the help handler
helpHandler: Help = Help(logger=helpLogger)

# Create the bot
logger.debug("Creating bot")
intents: Intents = Intents.default()
bot: Bot = Bot(intents=intents)


# Create bot commands
@bot.command(
    name="ping",
    description="Get the bot's latency.",
    aliases=["latency"],
    usage="ping",
)
async def _ping(ctx: ApplicationContext) -> None:
    """
    Get the bot's latency.

    Args:
        ctx (ApplicationContext): Context of the command.

    Returns:
        None
    """
    # Send the latency
    logger.info(f"_ping: Sending latency message to {ctx.author}")
    await ctx.respond(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)


@bot.command(
    name="help",
    description="Get the bot's help message.",
    usage="help [command]",
)
@option(name="command", description="The command to get help for.", type=str, required=False)
async def _help(ctx: ApplicationContext, command: str = None) -> None:
    """
    Get the bot's help message.

    Args:
        ctx (ApplicationContext): Context of the command.
        command (str): The command to get help for.

    Returns:
        None
    """
    logger.info(f"_help: Sending help message to {ctx.author} for command {command}")
    # Get the help message
    if command is None:
        await ctx.respond(ephemeral=True)

    # Get the appropriate help embed
    embed: Embed = helpHandler.getHelp(command)

    # Send the help message
    await ctx.respond(embed=embed, ephemeral=True)

# Run the bot
if __name__ == "__main__":
    # Start the bot
    logger.debug("Starting bot")
    bot.run(token)
