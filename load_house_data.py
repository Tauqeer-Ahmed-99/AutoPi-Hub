import json
from typing import List

from database.actions import add_user, create_device, create_room, init_house_db
from database.database import get_db
from database.db_models import Device, DeviceControlLog, HouseMember
from helpers.data_models import House, HouseMember as HouseMemberData, DeviceControlLog as DeviceControlLogData
from sqlalchemy.exc import SQLAlchemyError

logs: List[DeviceControlLogData]

with open('data/logs.json', 'r', encoding='utf-8') as f:
    logs = json.load(f)

print("[Loaded] Device Control Logs")


with open('data/house_data.json', 'r', encoding='utf-8') as f:
    house_data: House = json.load(f)
    house = init_house_db(house_data.house_password_hash)

    if isinstance(house, SQLAlchemyError):
        raise Exception(house._message())

    for room in house.rooms:
        room = create_room(room.room_name, house.house_id)

        if isinstance(room, SQLAlchemyError):
            raise Exception(room._message())

        for device in room.devices:
            # device = create_device(device.device_name, device.pin_number, room.room_id)
            db = get_db()
            try:
                with db.begin() as txn:
                    new_device = Device(deviceName=device.device_name, pinNumber=device.pin_number,
                                        roomId=room.room_id, status=device.status, isScheduled=device.is_scheduled,
                                        isDefault=device.is_default, daysScheduled=device.days_scheduled, startTime=device.start_time, offTime=device.off_time, scheduledBy=device.scheduled_by
                                        )
                    db.add(new_device)
                    db.flush()
                    for log in logs:
                        if log.device_id == device.device_id:
                            new_log = DeviceControlLog(statusChangedFrom=log.status_changed_from,
                                                       statusChangedTo=log.status_changed_to,
                                                       deviceId=new_device.get_data().device_id,
                                                       userId=log.user_id)

                            if isinstance(new_log, SQLAlchemyError):
                                raise Exception(new_log._message())
            except SQLAlchemyError as SQLError:
                print("[DB] Device Creation Failed.")
                print(SQLError)
            finally:
                db.close()

print("[Loaded] House Data")

with open('data/house_members.json', 'r', encoding='utf-8') as f:
    house_members_data: List[HouseMemberData] = json.load(f)

    for house_member in house_members_data:
        user = add_user(house_member.user_id)

        if isinstance(user, SQLAlchemyError):
            raise Exception(user._message())

print("[Loaded] House Members Data")
