from __future__ import annotations

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

async def _no_prefix(_bot: commands.Bot, _message: discord.Message) -> list[str]:
    return []


class PluvBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix=_no_prefix, intents=intents)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.pluv")
        await self.tree.sync()
        print("pluv synced")


bot = PluvBot()


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN", "").strip()
    if not token:
        raise SystemExit("set DISCORD_TOKEN in .env")
    bot.run(token)


if __name__ == "__main__":
    main()