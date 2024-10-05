import json
import threading
from datetime import datetime
from typing import Any, List
import asyncio

from database.actions import switch_device

from helpers.data_models import Device

from services.scheduled_device import get_scheduled_device_status
from services.socket import SocketEvents, SocketManager


class ScheduleDeviceAssistant():
    scheduled_devices: List[Device] = []
    controller_device: Any
    socket_manager: SocketManager

    stop_event: threading.Event
    worker_thread: threading.Thread | None = None

    def __init__(self, controller_device: Any, socket_manager: SocketManager):
        scheduled_devices = controller_device.get_scheduled_devices()
        scheduled_devices = scheduled_devices if scheduled_devices is not None else []
        self.scheduled_devices = scheduled_devices
        self.controller_device = controller_device
        self.socket_manager = socket_manager
        self.stop_event = threading.Event()

    def start_scheduled_devices_watch(self):
        # Stop the current worker thread if it is running
        if self.worker_thread is not None and self.worker_thread.is_alive():
            self.stop_event.set()
            self.worker_thread.join()

        # Clear the stop event for the new worker thread
        self.stop_event.clear()

        # Start a new worker thread
        self.worker_thread = threading.Thread(
            target=self._scheduled_devices_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def _scheduled_devices_worker(self):
        asyncio.run(self._scheduled_devices_worker_async())

    async def _scheduled_devices_worker_async(self):
        while not self.stop_event.is_set():
            await self.switch_scheduled_devices()
            # Wait for 60 seconds or until stop_event is set
            if not self.stop_event.wait(60):
                await asyncio.sleep(0)

    async def switch_scheduled_devices(self):
        today = datetime.now().strftime("%a")
        for device in self.scheduled_devices:
            if today.lower() in device.days_scheduled.lower() if device.days_scheduled is not None else "":
                is_on = get_scheduled_device_status(
                    device.start_time if device.start_time is not None else "",
                    device.off_time if device.off_time is not None else "")
                if is_on != device.status:
                    device.status = is_on
                    try:
                        self.controller_device.switch_device(
                            device.device_id, is_on)
                        broadcast_data = {
                            "event": SocketEvents.SCHEDULED_SWITCH_DEVICE,
                            "user_id": f"{device.scheduled_by}|-|Schedule Assistant",
                            "message": f"Schedule Assistant turned {'on' if is_on else 'off'} {device.device_name}.",
                            "data": {"deviceId": device.device_id, "state": is_on}
                        }
                        await self.socket_manager.broadcast(json.dumps(broadcast_data))
                        switch_device(device.device_id, device.status, is_on,
                                      f"{device.scheduled_by}|-|Schedule Assistant")
                    except Exception as e:
                        print(
                            f"[Schedule Assistant] : Switch scheduled device failed. {e}")

    def schedule_device(self, device: Device):
        self.remove_scheduled_device(device.device_id)
        self.scheduled_devices.append(device)
        # Restart the watch only if the worker thread is not already running
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.start_scheduled_devices_watch()

    def get_scheduled_device(self, device_id: str):
        for device in self.scheduled_devices:
            if device.device_id == device_id:
                return device

    def remove_scheduled_device(self, device_id: str):
        device = self.get_scheduled_device(device_id)
        if device is not None:
            self.scheduled_devices.remove(device)
            # Restart the watch only if there are scheduled devices left
            if len(self.scheduled_devices) > 0:
                self.start_scheduled_devices_watch()
            else:
                self.stop_scheduled_devices_watch()

    def stop_scheduled_devices_watch(self):
        if self.worker_thread is not None and self.worker_thread.is_alive():
            self.stop_event.set()
            self.worker_thread.join()
