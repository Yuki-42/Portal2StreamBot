"""
Contains the help handling logic for the bot.
"""

# Standard Library
from json import load
from pathlib import Path

# Third Party
from discord import Embed, Colour

# Local
from ._logging import SuppressedLoggerAdapter


class Help:
    """
    Help message constructor and handler.
    """
    # Type Hints
    logger: SuppressedLoggerAdapter
    file: dict[str, dict[str, str]]

    def __init__(self, logger: SuppressedLoggerAdapter, helpFile: str | Path = Path("help.json")) -> None:
        """
        Constructor for the Help class.

        Args:
            helpFile (str | Path): The file to load the help message from.
        """
        # Set the logger
        self.logger = logger

        # Load the help message
        self.logger.debug("Loading help messages")
        with open(helpFile, "r") as file:
            self.file: dict = load(file)

    def _getCommand(self, command: str) -> dict[str, str]:
        """
        Get the help data for a command.

        Args:
            command (str): The command to get the help message for.

        Returns:
            dict[str, str]: The help data for the command.
        """
        try:
            # Get the help message
            return self.file.get(command)
        except KeyError:
            # Return a default help message
            return {
                "name": "Command Not Found",
                "description": f"The command {command} does not exist.",
            }

    @staticmethod
    def _constructEmbed(data: dict[str, str | list[str]]) -> Embed:
        """
        Construct an embed from the help data.

        Args:
            data (dict[str, str]): The help data to construct the embed from.

        Returns:
            Embed: The embed constructed from the help data.
        """
        # Construct the base embed with required fields
        embed: Embed = Embed(
            title=data.get("name"),
            description=data.get("description"),
            colour=Colour.random(),
        )

        # Add the usage field if it exists
        if usage := data.get("usage"):
            embed.add_field(name="Usage", value=usage, inline=False)

        # Add the aliases field if it exists
        if aliases := data.get("aliases"):
            embed.add_field(name="Aliases", value=", ".join(aliases), inline=False)

        return embed

    def getHelp(self, command: str) -> Embed:
        """
        Get the help message for a command.

        Args:
            command (str): The command to get the help message for.

        Returns:
            Embed: The help message for the command.
        """
        # Get the appropriate help embed
        self.logger.debug(f"Getting help for command {command}")
        return self._constructEmbed(self._getCommand(command))
