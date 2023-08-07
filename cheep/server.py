import asyncio
from datetime import datetime

from cheep.device import Device, get_on_device
from cheep.utils import speak, turn_off_plug


async def turn_off_plug_if_needed(passed_time: int, device: Device) -> bool:
    if device != Device.WII_U or passed_time <= 25:
        return False
    await speak("将在2分钟后关闭插座")
    await asyncio.sleep(2 * 60)
    await turn_off_plug()
    return True


async def device_alert(passed_time: int, waiting_time: int) -> int:
    """
    :return: 0 if plug closed, otherwise passed_time
    """
    await asyncio.sleep(waiting_time * 60)
    device = await get_on_device()
    if not device:
        return 0
    passed_time += waiting_time
    alert_message = f"你已经使用了{passed_time}分钟的{device.value}了"
    await speak(alert_message)
    if await turn_off_plug_if_needed(passed_time, device):
        return 0
    return passed_time


async def count_down(device: Device):
    await speak(f"{device.value}开了")
    started_on = datetime.now()
    print(f"{device.name} opened on {started_on.strftime('%Y %H:%M')}")
    passed_time = 0
    if (passed_time := await device_alert(passed_time, 15)) == 0:
        return
    while passed_time := await device_alert(passed_time, 5):
        pass
    print(
        f"tv closed on {datetime.now().strftime('%Y %H:%M')},"
        f"{datetime.now() - started_on}"
    )


async def main():
    while True:
        device = await get_on_device()
        if device:
            await count_down(device)
        await asyncio.sleep(60)
