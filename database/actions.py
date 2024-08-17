
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from database.database import get_db
from database.db_models import Houses, HouseMember, Room, Device, DeviceControlLog
from helpers.data_models import HouseMember as HouseMemberData, Room as RoomData, Device as DeviceData, House as HouseData

from services.scheduled_device import get_scheduled_device_status


def get_user(user_id: str) -> HouseMemberData | None | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:  # Automatically handles commit/rollback
            # Use `first()` to avoid IndexError
            house_member = db.query(HouseMember).filter(
                HouseMember.userId == user_id).first()
            db.flush()
            user = house_member.get_data() if house_member is not None else None
            return user
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieving User Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_access(user_id: str) -> bool | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:  # Automatically handles commit/rollback
            # Use `first()` to avoid IndexError
            house = db.query(Houses).first()
            if house is None:
                print("[DB] House not initialized.")
                raise Exception(SQLAlchemyError)

            # Query for access
            access = db.query(HouseMember).filter(
                HouseMember.houseId == house.houseId,
                HouseMember.userId == user_id
            ).first()  # Use `first()` to get the result or None

            db.flush()
            return bool(access)  # Return True if access is found
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieving Access Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def create_room(room_name: str, house_id: str) -> RoomData | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            new_room = Room(roomName=room_name, houseId=house_id)
            db.add(new_room)
            db.flush()
            return new_room.get_data()
    except SQLAlchemyError as SQLError:
        print("[DB] Room Creation Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def remove_room(room_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin()as txn:
            count = db.query(Room).filter(Room.roomId == room_id).delete()
            print(f"[DB] {count} Room(s) Deleted.")
            db.flush()
            return count
    except SQLAlchemyError as SQLError:
        print("[DB] Room Deleting Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def create_device(device_name: str, pin_number: int, room_id: str) -> DeviceData | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            new_device = Device(deviceName=device_name, pinNumber=pin_number,
                                roomId=room_id, status=False, isScheduled=False)
            db.add(new_device)
            db.flush()
            return new_device.get_data()
    except SQLAlchemyError as SQLError:
        print("[DB] Device Creation Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def switch_device(device_id: str, from_status: bool, to_status: bool, user_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            count = db.query(Device).filter(Device.deviceId == device_id).update(
                {
                    Device.status: to_status
                }
            )
            db.add(DeviceControlLog(statusChangedFrom=from_status,
                                    statusChangedTo=to_status,
                                    deviceId=device_id,
                                    userId=user_id))
            db.flush()
            return count
    except SQLAlchemyError as SQLError:
        print("[DB] Switch Device Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def configure_device(device_id: str, device_name: str, pin_number: int, status: bool, is_scheduled: bool,
                     days_scheduled: str, start_time: str, off_time: str, user_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            device = db.query(Device).filter(Device.deviceId == device_id)
            old_status = getattr(device.first(), "status", None)
            new_status = get_scheduled_device_status(start_time, off_time)
            count = device.update(
                {
                    Device.deviceName: device_name,
                    Device.pinNumber: pin_number,
                    Device.isScheduled: is_scheduled,
                    Device.daysScheduled: days_scheduled if is_scheduled else "",
                    Device.startTime: start_time if is_scheduled else "",
                    Device.offTime: off_time if is_scheduled else "",
                    Device.status: new_status if is_scheduled else status,
                    Device.scheduledBy: user_id
                }
            )
            if old_status != new_status:
                db.add(DeviceControlLog(statusChangedFrom=old_status,
                                        statusChangedTo=new_status,
                                        deviceId=device_id,
                                        userId=user_id))
            db.flush()
            return count
    except SQLAlchemyError as SQLError:
        print("[DB] Switch Device Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def remove_device(device_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            count = db.query(Device).filter(
                Device.roomId == device_id).delete()
            print(f"[DB] {count} Device(s) Deleted.")
            db.flush()
            return count
    except SQLAlchemyError as SQLError:
        print("[DB] Device Deleting Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_house_data() -> HouseData | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            house = db.query(Houses).first()
            if house is None:
                print("[DB] House not initialized.")
                raise Exception(SQLAlchemyError)
            return house.get_data()
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieve House Data Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_scheduled_devices() -> List[DeviceData] | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            scheduled_devices = db.query(Device).filter(
                Device.isScheduled == True)
            return [device.get_data() for device in scheduled_devices]
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieve Scheduled Devices Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()
