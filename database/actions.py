
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from database.database import get_db
from database.db_models import Houses, HouseMember, Room, Device, DeviceControlLog
from helpers.data_models import HouseMember as HouseMemberData, Room as RoomData, Device as DeviceData, House as HouseData

from services.scheduled_device import get_scheduled_device_status

from helpers.header_pins import HeaderPinType, HeaderPinConfigDataModel, pin_header_config


def init_house_db(house_password_hash: str):
    db = get_db()
    try:
        with db.begin() as txn:  # Automatically handles commit/rollback
            # Use `first()` to avoid IndexError
            new_house = Houses(houseName="My House",
                               passwordHash=house_password_hash)
            db.add(new_house)
            db.flush()
            return new_house.get_data()
    except SQLAlchemyError as SQLError:
        print("[DB] Initializing House Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_house() -> HouseData | None | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:  # Automatically handles commit/rollback
            # Use `first()` to avoid IndexError
            house = db.query(Houses).first()
            if house is None:
                print("[House] House is not initialized.")
            db.flush()
            return house.get_data() if house is not None else None
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieving House Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def add_user(user_id: str) -> HouseMemberData | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:  # Automatically handles commit/rollback
            # Use `first()` to avoid IndexError
            house = db.query(Houses).first()
            if house is None:
                raise SQLAlchemyError("[House] House is not initialized.")
            house_member = db.query(HouseMember).filter(
                HouseMember.houseId == house.houseId, HouseMember.userId == user_id).first()
            if house_member is not None:
                return house_member.get_data()
            new_house_member = HouseMember(
                userId=user_id, houseId=house.houseId)
            db.add(new_house_member)
            db.flush()
            return new_house_member.get_data()
    except SQLAlchemyError as SQLError:
        print("[DB] Adding House Member Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_house_members() -> List[HouseMemberData] | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            house_members = db.query(HouseMember).all()
            db.flush()
            return [house_member.get_data() for house_member in house_members]
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieving House Members Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


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


def delete_user(user_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            delete_count = db.query(HouseMember).filter(
                HouseMember.userId == user_id).delete()
            db.flush()
            return delete_count
    except SQLAlchemyError as SQLError:
        print("[DB] Deleting User Failed.")
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
            current_default_device = db.query(Device).filter(
                Device.roomId == room_id, Device.isDefault == True).first()
            new_device = Device(deviceName=device_name, pinNumber=pin_number,
                                roomId=room_id, status=False, isScheduled=False, isDefault=True if current_default_device is None else False)
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


def configure_device(device_id: str, device_name: str, pin_number: int, status: bool, is_default: bool, is_scheduled: bool,
                     days_scheduled: str, start_time: str, off_time: str, user_id: str) -> int | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            device = db.query(Device).filter(Device.deviceId == device_id)
            current_device = device.first()

            # If current device is set a sdefault then remove all other devices from default devices of the room
            old_is_default = getattr(current_device, "isDefault", None)
            is_new_default = old_is_default != None and old_is_default != is_default
            if is_new_default and current_device is not None:
                db.query(Device).filter(Device.roomId == current_device.roomId, Device.isDefault == True).update({
                    Device.isDefault: False
                })

            new_status = get_scheduled_device_status(
                start_time, off_time) if is_scheduled else status
            count = device.update(
                {
                    Device.deviceName: device_name,
                    Device.pinNumber: pin_number,
                    Device.isScheduled: is_scheduled,
                    Device.daysScheduled: days_scheduled if is_scheduled else "",
                    Device.startTime: start_time if is_scheduled else "",
                    Device.offTime: off_time if is_scheduled else "",
                    Device.status: new_status,
                    Device.isDefault: is_default,
                    Device.scheduledBy: user_id
                }
            )

            old_status = getattr(current_device, "status", None)
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
                Device.deviceId == device_id).delete()
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


def get_available_gpio_pins() -> List[HeaderPinConfigDataModel] | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            all_devices = db.query(Device).all()
            used_gpio_pins = [int(str(device.pinNumber))
                              for device in all_devices]
            available_gpio_pins: List[HeaderPinConfigDataModel] = []

            for pin_config in pin_header_config:
                if pin_config.type == HeaderPinType.GPIO and pin_config.gpio_pin_number not in used_gpio_pins:
                    available_gpio_pins.append(pin_config.get_data())

            return available_gpio_pins
    except SQLAlchemyError as SQLError:
        print("[DB] Retrieve Scheduled Devices Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()


def get_device_control_logs() -> List[DeviceControlLog] | SQLAlchemyError:
    db = get_db()
    try:
        with db.begin() as txn:
            logs = db.query(DeviceControlLog).all()
            db.flush()
            return logs
    except SQLAlchemyError as SQLError:
        print("[DB] Device Creation Failed.")
        print(SQLError)
        return SQLError
    finally:
        db.close()
