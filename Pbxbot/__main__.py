import asyncio
import sys

from Pbxbot.clients import Pbxbot
from Pbxbot.config import Config, Symbols
from Pbxbot.logger import LOGS
from Pbxbot.functions.tools import initialize_git
from Pbxbot.functions.initializer import (
    UserSetup,
    ForcesubSetup,
    GachaBotsSetup,
    TemplateSetup,
)


async def startup_sequence():
    LOGS.info(f"{Symbols.bullet * 3} Starting Pbxbot... {Symbols.bullet * 3}")

    # Step 1: Initialize users, bans, stans, etc.
    await UserSetup()

    # Step 2: Setup forcesub chats
    await ForcesubSetup()

    # Step 3: Setup GachaBot IDs
    await GachaBotsSetup()

    # Step 4: Load templates
    await TemplateSetup()

    # Step 5: (Optional) Git initialization
    if Config.GIT_REPO:
        success, repo, force = await initialize_git(Config.GIT_REPO)
        if success:
            LOGS.info(f"{Symbols.check} Git initialized successfully.")
        else:
            LOGS.warning(f"{Symbols.cross} Git not initialized: {repo}")


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(startup_sequence())
        Pbxbot.run()
    except (KeyboardInterrupt, SystemExit):
        LOGS.info(f"{Symbols.cross} Exiting Pbxbot...")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
