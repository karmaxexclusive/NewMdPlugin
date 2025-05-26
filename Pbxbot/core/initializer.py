import sys
from types import ModuleType
from .clients import Pbxbot
from .config import Config, Symbols
from .database import db
from .logger import LOGS


async def _AuthUsers() -> None:
    """Authorize Owner, all bot clients, and stan users."""
    users = {Config.OWNER_ID}
    users.update([(await client.get_me()).id for client in Pbxbot.users])

    stan_users = await db.get_all_stans()
    users.update(user["user_id"] for user in stan_users)

    Config.AUTH_USERS.update(users)

    LOGS.info(f"{Symbols.arrow_right * 2} Added Authorized Users {Symbols.arrow_left * 2}")


async def _StanUsers() -> None:
    """Add stan users to config."""
    users = await db.get_all_stans()
    Config.STAN_USERS.update(user["user_id"] for user in users)

    LOGS.info(f"{Symbols.arrow_right * 2} Added Stan Users {Symbols.arrow_left * 2}")


async def _GbanUsers() -> None:
    """Add global ban and mute users to config."""
    banned = await db.get_gban()
    Config.BANNED_USERS.update(user["user_id"] for user in banned)
    LOGS.info(f"{Symbols.arrow_right * 2} Added {len(banned)} Gbanned Users {Symbols.arrow_left * 2}")

    muted = await db.get_gmute()
    Config.MUTED_USERS.update(user["user_id"] for user in muted)
    LOGS.info(f"{Symbols.arrow_right * 2} Added {len(muted)} Gmuted Users {Symbols.arrow_left * 2}")


async def UserSetup() -> None:
    """Initialize all user-related config values."""
    LOGS.info(f"{Symbols.bullet * 3} Setting Up Users {Symbols.bullet * 3}")
    await _AuthUsers()
    await _StanUsers()
    await _GbanUsers()


async def ForcesubSetup() -> None:
    """Initialize force subscription chats."""
    chats = await db.get_all_forcesubs()
    Config.FORCESUBS.update(chat["chat"] for chat in chats)


async def GachaBotsSetup() -> None:
    """Initialize registered GachaBot IDs."""
    bots = await db.get_all_gachabots_id()
    Config.GACHA_BOTS.update(bots)


async def TemplateSetup() -> None:
    """Load uppercase template constants from template file into config."""
    module_name = "temp_module"
    module: ModuleType = sys.modules.get(module_name) or type(sys)(module_name)

    try:
        with open("Pbxbot/functions/templates.py", "r", encoding="utf-8") as file:
            exec(file.read(), module.__dict__)
    except FileNotFoundError:
        LOGS.error("Template file not found: Pbxbot/functions/templates.py")
        return
    except Exception as e:
        LOGS.error(f"Failed to load templates: {e}")
        return

    global_vars = module.__dict__
    Config.TEMPLATES = {
        var: global_vars[var][0]
        for var in global_vars
        if var.isupper() and not callable(global_vars[var]) and isinstance(global_vars[var], (list, tuple))
    }
