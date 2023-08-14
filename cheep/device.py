from enum import Enum
from typing import Union

from cheep.utils import get_plug_w


class Device(str, Enum):
    TV = "电视"  # 100w
    WII_U = "游戏机"  # 100w + 35w


async def get_on_device() -> Union[Device, None]:
    w = await get_plug_w()
    if w > 120:
        return Device.WII_U
    if w > 90:
        return Device.TV
    return None
