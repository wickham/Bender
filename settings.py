import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord


load_dotenv()
DISCORD_API_SECRET = os.getenv("DISCORD_TOKEN")
DADJOKESAPI = os.getenv("DADJOKESAPI")
ROLE_POWER_TRIP = os.getenv("ROLE_POWER_TRIP")


BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

VIDEOCMDS_DIR = BASE_DIR / "videocmds"

GUILDS_ID = discord.Object(id=int(os.getenv("DISCORD_GUILD")))
FEEDBACK_CH = int(os.getenv("FEEDBACK_CH", 0))
GUILD_ID_INT = int(os.getenv("DISCORD_GUILD"))

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - [%(asctime)s] - %(module)-15s : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {
            "format": "%(levelname)-10s - [%(asctime)s] - %(name)-15s : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/history.log",
            "mode": "w",
            "formatter": "verbose",
            "maxBytes": 1024,
            "backupCount": 5,
        },
    },
    "loggers": {
        "bot": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        "cog": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
