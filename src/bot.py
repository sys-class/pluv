from __future__ import annotations

import os
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
IMAGE = ROOT / "pluv.png"


async def _no_prefix(_bot: commands.Bot, _message: discord.Message) -> list[str]:
    return []


class PluvBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix=_no_prefix, intents=intents)

    async def setup_hook(self) -> None:
        await self.tree.sync()
        print('pluv synced')


bot = PluvBot()


@bot.tree.command(name="pluv", description="send pluv")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_pluv(interaction: discord.Interaction) -> None:
    if not IMAGE.is_file():
        await interaction.response.send_message(
            "pluv.png not found", ephemeral=True
        )
        return
    await interaction.response.send_message(file=discord.File(IMAGE))


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    if bot.user and bot.user in message.mentions:
        if not IMAGE.is_file():
            await message.reply("pluv.png not found")
            return
        await message.reply(file=discord.File(IMAGE))


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN", "").strip()
    if not token:
        raise SystemExit("set DISCORD_TOKEN in .env")
    bot.run(token)


if __name__ == "__main__":
    main()