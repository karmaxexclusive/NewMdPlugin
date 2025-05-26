import asyncio
import contextlib
import math
import os
import shlex
import shutil
import time

from pyrogram.types import Message
from Pbxbot.core import Config, Symbols
from .formatter import humanbytes, readable_time

# Try importing GitPython if git is available
if shutil.which("git"):
    from git import Repo
    from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
else:
    Repo = None
    GitCommandError = InvalidGitRepositoryError = NoSuchPathError = Exception


async def progress(current: int, total: int, message: Message, start: float, process: str):
    now = time.time()
    diff = now - start
    if round(diff % 10.0) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        complete_time = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + complete_time

        progress_str = "**[{0}{1}] : {2}%**\n".format(
            "●" * math.floor(percentage / 10),
            "○" * (10 - math.floor(percentage / 10)),
            round(percentage, 2)
        )

        msg = (
            f"{progress_str}"
            f"__{humanbytes(current)}__ **of** __{humanbytes(total)}__\n"
            f"**Speed:** __{humanbytes(speed)}/s__\n"
            f"**ETA:** __{readable_time(estimated_total_time / 1000)}__"
        )

        await message.edit_text(f"**{process} ...**\n\n{msg}")


async def get_files_from_directory(directory: str) -> list[str]:
    return [
        os.path.join(path, file)
        for path, _, files in os.walk(directory)
        for file in files
    ]


async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def update_dotenv(key: str, value: str) -> None:
    try:
        with open(".env", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                break
        else:
            lines.append(f"{key}={value}\n")

        with open(".env", "w") as file:
            file.writelines(lines)
    except Exception as e:
        print(f"Failed to update .env: {e}")


async def restart(update: bool = False, clean_up: bool = False, shutdown: bool = False):
    with contextlib.suppress(Exception):
        shutil.rmtree(Config.DWL_DIR)
        shutil.rmtree(Config.TEMP_DIR)

    if clean_up:
        os.makedirs(Config.DWL_DIR, exist_ok=True)
        os.makedirs(Config.TEMP_DIR, exist_ok=True)
        return

    if shutdown:
        os.system(f"kill -9 {os.getpid()}")
        return

    cmd = (
        "git pull && pip3 install -U -r requirements.txt && bash start.sh"
        if update else
        "bash start.sh"
    )
    os.system(f"kill -9 {os.getpid()} && {cmd}")


async def gen_changelogs(repo: Repo, branch: str) -> str:
    changelogs = ""
    try:
        commits = list(repo.iter_commits(branch))[:5]
        for index, commit in enumerate(commits):
            changelogs += f"**{Symbols.triangle_right} {index + 1}.** `{commit.summary}`\n"
    except Exception as e:
        changelogs = f"Error generating changelogs: {e}"
    return changelogs


async def initialize_git(git_repo: str) -> tuple[bool, object, bool]:
    if Repo is None:
        return False, "Git not available in environment", False

    force = False
    try:
        repo = Repo()
    except (NoSuchPathError, GitCommandError) as err:
        return False, err, force
    except InvalidGitRepositoryError:
        try:
            repo = Repo.init()
            origin = repo.create_remote("upstream", f"https://github.com/{git_repo}")
            origin.fetch()
            repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            force = True
        except Exception as e:
            return False, e, force

    with contextlib.suppress(Exception):
        repo.create_remote("upstream", f"https://github.com/{git_repo}")

    return True, repo, force
