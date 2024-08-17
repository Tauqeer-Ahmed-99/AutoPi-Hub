from typing import List
from gpiozero import OutputDevice

from sqlalchemy.exc import SQLAlchemyError

from database.actions import get_house_data
from helpers.data_models import House, Room, Device


class ControllerDevice:

    house: House | None = None

    def __init__(self):
        try:
            self.load_data()
            self.initialize_output_devices()
        except Exception as e:
            print(f"Error initializing ControllerDevice: {e}")
            raise

    def load_data(self):
        try:
            data = get_house_data()
            if isinstance(data, SQLAlchemyError):
                raise Exception(
                    "[Controller] [DB] Unable to load controller data.")
            self.house = data
        except Exception as e:
            print(f"Error in load_data: {e}")

    def initialize_output_devices(self):
        try:
            if self.house is not None:
                for room in self.house.rooms:
                    for device in room.devices:
                        device.output_device = OutputDevice(
                            device.pin_number, active_high=False)
        except Exception as e:
            print(f"Error initializing output devices: {e}")
            raise

    def add_room(self, room: Room):
        if self.house is not None:
            self.house.rooms.append(room)

    def get_room(self, id: str):
        try:
            if self.house is not None:
                for room in self.house.rooms:
                    if room.room_id == id:
                        return room
        except Exception as e:
            print(f"Error getting room: {e}")
            return None

    def remove_room(self, room_id: str):
        if self.house is not None:
            room = self.get_room(room_id)
            if room is not None:
                for device in room.devices:
                    if device.output_device is not None:
                        device.output_device.close()
                self.house.rooms.remove(room)

    def add_device(self, device: Device):
        room = self.get_room(device.room_id)
        if room is not None:
            device.output_device = OutputDevice(
                device.pin_number, active_high=False)
            room.devices.append(device)

    def get_device(self, id: str):
        try:
            if self.house is not None:
                for room in self.house.rooms:
                    for device in room.devices:
                        if device.device_id == id:
                            return device
        except Exception as e:
            print(f"Error getting device: {e}")
            return None

    def get_scheduled_devices(self) -> List[Device] | None:
        scheduled_devices: List[Device] = []
        if self.house is not None:
            for room in self.house.rooms:
                for device in room.devices:
                    if device.is_scheduled:
                        scheduled_devices.append(device)
            return scheduled_devices

    def switch_device(self, id: str, status: bool):
        try:
            device = self.get_device(id)
            output_device = device.output_device if device is not None else None
            if output_device is not None:
                if status:
                    output_device.on()
                else:
                    output_device.off()
            else:
                if device is None:
                    raise Exception(f"Device with id '{id}' not found.")
                if output_device is None:
                    raise Exception(f"Output Device is not initialized.")
        except Exception as e:
            print(f"Error switching device: {e}")
            raise

    def remove_device(self, device_id):
        device = self.get_device(device_id)
        if device is not None:
            output_device = device.output_device
            if output_device is not None:
                output_device.close()
            room = self.get_room(device.device_id)
            if room is not None:
                room.devices.remove(device)
