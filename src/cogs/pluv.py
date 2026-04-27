from __future__ import annotations

import random
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

ROOT = Path(__file__).resolve().parent.parent.parent
IMAGE = ROOT / "pluv.png"
PLUVS_DIR = ROOT / "src" / "pluvs"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


class PluvCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="pluv", description="send pluv")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def slash_pluv(self, interaction: discord.Interaction) -> None:
        if not IMAGE.is_file():
            await interaction.response.send_message(
                "pluv.png not found", ephemeral=True
            )
            return
        await interaction.response.send_message(file=discord.File(IMAGE))

    @app_commands.command(name="randompluv", description="send random pluv")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def slash_random_pluv(self, interaction: discord.Interaction) -> None:
        if not PLUVS_DIR.is_dir():
            await interaction.response.send_message(
                "pluvs folder not found", ephemeral=True
            )
            return

        images = [
            path
            for path in PLUVS_DIR.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ]
        if not images:
            await interaction.response.send_message(
                "no images found in pluvs folder", ephemeral=True
            )
            return

        await interaction.response.send_message(file=discord.File(random.choice(images)))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if self.bot.user and self.bot.user in message.mentions:
            if not IMAGE.is_file():
                await message.reply("pluv.png not found")
                return
            await message.reply(file=discord.File(IMAGE))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PluvCog(bot))
