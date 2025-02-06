import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from aiohttp import ClientSession
from dotenv import load_dotenv
from miservice import MiAccount, MiIOService, miio_command

load_dotenv()


async def speak(text: str):
    did = os.environ.get("SPEAKER_DID")
    assert did is not None
    return await exec_cmd(did, f"5 {text}")


async def get_plug_w() -> int:
    did = os.environ.get("PLUG_DID")
    assert did is not None
    return (await exec_cmd(did, "11-2", default_value=[0]))[0]


async def turn_off_plug():
    did = os.environ.get("PLUG_DID")
    assert did is not None
    await exec_cmd(did, "2-1=false")


async def _exec_cmd(did: str, args: str):
    async with ClientSession() as session:
        account = MiAccount(
            session,
            os.environ.get("MI_USER"),
            os.environ.get("MI_PASS"),
            os.path.join(str(Path.home()), ".mi.token"),
        )
        service = MiIOService(account)
        return await miio_command(service, did, args, f"{sys.argv[0]} ")


async def exec_cmd(did: str, args: str, default_value: Any = None):
    for i in range(3):
        try:
            return await _exec_cmd(did, args)
        except Exception as e:
            print(f"did: {did}, exec_cmd error: {e}, retry {i + 1}...")
            await asyncio.sleep(9)
    print(f"did: {did}, exec_cmd failed, return default value: default_value")
    return default_value
