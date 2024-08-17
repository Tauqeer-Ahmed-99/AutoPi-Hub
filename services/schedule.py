import threading
from datetime import datetime
from typing import List

from database.actions import switch_device

from helpers.data_models import Device

from services.scheduled_device import get_scheduled_device_status


def set_interval(func, sec):
    def wrapper():
        set_interval(func, sec)  # Schedule the next call
        func()  # Call the function

    t = threading.Timer(sec, wrapper)
    t.start()
    return t


class ScheduleDeviceAssistant():

    scheduled_devices: List[Device] = []

    _timer: threading.Timer

    def __init__(self, scheduled_devices: List[Device]):
        self.scheduled_devices = scheduled_devices

    def start_scheduled_devices_watch(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = set_interval(self.switch_scheduled_device, 60)

    def switch_scheduled_device(self):
        today = datetime.now().strftime("%a")
        for device in self.scheduled_devices:
            if today.lower() in device.days_scheduled.lower():
                is_on = get_scheduled_device_status(
                    device.start_time, device.off_time)
                if is_on != device.status:
                    device.status = is_on

                    switch_device(device.device_id, device.status, is_on,
                                  f"{device.scheduled_by}|-|Schedule Assistant")

    def schedule_device(self, device: Device):
        self.remove_scheduled_device(device.device_id)
        self.scheduled_devices.append(device)
        self.start_scheduled_devices_watch()

    def get_scheduled_device(self, device_id: str):
        for device in self.scheduled_devices:
            if device.device_id == device_id:
                return device

    def remove_scheduled_device(self, device_id: str):
        device = self.get_scheduled_device(device_id)
        if device is not None:
            self.scheduled_devices.remove(device)
            self.start_scheduled_devices_watch()
