import asyncio
from datetime import datetime, timedelta

from cheep.device import Device, get_on_device
from cheep.utils import speak, turn_off_plug


def is_parents_in_home():
    now = datetime.now()
    return now.hour >= 19 or now.weekday() >= 5


async def turn_off_plug_if_needed(passed_time: int, device: Device) -> bool:
    if device != Device.WII_U or passed_time <= 25 or is_parents_in_home():
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


async def count_down(device: Device, latest_tv_watch_time: datetime) -> timedelta:
    def end():
        print(
            f"{device.name} closed on {datetime.now().strftime('%Y-%m-%d %H:%M')},"
            f"{datetime.now() - started_on}"
        )
        return datetime.now() - started_on

    if (datetime.now() - latest_tv_watch_time) < timedelta(
        minutes=30
    ) and not is_parents_in_home():
        await speak("请先休息30分钟眼睛后再看电视")
        await turn_off_plug()
        return timedelta()

    await speak(f"{device.value}开了")
    started_on = datetime.now()
    print(f"{device.name} opened on {started_on.strftime('%Y-%m-%d %H:%M')}")
    passed_time = 0
    if (passed_time := await device_alert(passed_time, 15)) == 0:
        return end()
    while passed_time := await device_alert(passed_time, 5):
        pass
    return end()


async def main():
    latest_tv_watch_time = datetime.now()
    while True:
        device = await get_on_device()
        if device and (
            await count_down(device, latest_tv_watch_time)
        ).total_seconds() > (60 * 20):
            latest_tv_watch_time = datetime.now()
        await asyncio.sleep(60)
