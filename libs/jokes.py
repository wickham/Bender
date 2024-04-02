import json
import requests
import settings
import discord
from constants import *


def get_joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": settings.DADJOKESAPI,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers)
    assert json.loads(response.text)["success"], "No response from the joke server..."
    return json.loads(response.text)["body"][0]


def tell_joke():
    joke = get_joke()
    embedQ = discord.Embed(
        title="Question", url="", description=joke["setup"], color=0xEB4634
    )
    embedA = discord.Embed(
        title="Answer", url="", description=joke["punchline"], color=0x345EEB
    )
    return embedQ, embedA
