from typing import List

from gpiozero import OutputDevice


class Device():
    device_id: str
    device_name: str
    pin_number: int
    status: bool
    room_id: str
    is_scheduled: bool = False
    days_scheduled: str | None = None
    start_time: str | None = None
    off_time: str | None = None
    scheduled_by: str | None = None
    created_at: str
    updated_at: str
    output_device: OutputDevice | None = None

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "pin_number": self.pin_number,
            "status": self.status,
            "room_id": self.room_id,
            "is_scheduled": self.is_scheduled,
            "days_scheduled": self.days_scheduled,
            "start_time": self.start_time,
            "off_time": self.off_time,
            "scheduled_by": self.scheduled_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            # "output_device": self.output_device.__dict__ if self.output_device else None
        }


class Room():
    room_id: str
    room_name: str
    house_id: str
    created_at: str
    updated_at: str
    devices: List[Device]

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_name": self.room_name,
            "house_id": self.house_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "devices": [device.to_dict() for device in self.devices]
        }


class House():
    house_id: str
    house_name: str
    house_password_hash: str
    created_at: str
    updated_at: str
    rooms: List[Room]

    def to_dict(self):
        return {
            "house_id": self.house_id,
            "house_name": self.house_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "rooms": [room.to_dict() for room in self.rooms]
        }


class HouseMember():
    house_id: str
    user_id: str

    def to_dict(self):
        return {
            "house_id": self.house_id,
            "user_id": self.user_id
        }


class DeviceControlLog():
    device_control_log_id: str
    device_id: str
    user_id: str
    status_changed_from: bool
    status_changed_to: bool
    created_at: str
    updated_at: str

    def to_dict(self):
        return {
            "device_control_log_id": self.device_control_log_id,
            "device_id": self.device_id,
            "user_id": self.user_id,
            "status_changed_from": self.status_changed_from,
            "status_changed_to": self.status_changed_to,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
