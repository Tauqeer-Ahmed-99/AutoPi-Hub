from typing import List

from sqlalchemy import Column, Integer, Boolean, Numeric, Text, ForeignKey, DateTime, func, VARCHAR
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

from helpers.data_models import House, Room as RoomData, Device as DeviceData, HouseMember as HouseMemberData, DeviceControlLog as DeviceControlLogData


class Houses(Base):
    __tablename__ = 'House'

    houseId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    houseName = Column(Text, nullable=False)
    passwordHash = Column(Text, nullable=False)
    createdAt = Column(DateTime(timezone=True),
                       server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relationships
    rooms: Mapped[List["Room"]] = relationship('Room', back_populates='house',
                                               cascade='all, delete-orphan')

    def get_data(self):
        house = House()
        house.house_id = str(self.houseId)
        house.house_name = str(self.houseName)
        house.house_password_hash = str(self.passwordHash)
        house.created_at = str(self.createdAt)
        house.updated_at = str(self.updatedAt)
        house.rooms = [room.get_data() for room in self.rooms]
        return house


class HouseMember(Base):
    __tablename__ = 'HouseMembers'

    userId = Column(Text, nullable=False, primary_key=True)
    houseId = Column(UUID(as_uuid=True), ForeignKey(
        'House.houseId', ondelete='CASCADE'), nullable=False, primary_key=True)

    def get_data(self):
        house_member = HouseMemberData()
        house_member.house_id = str(self.houseId)
        house_member.user_id = str(self.userId)
        return house_member


class Room(Base):
    __tablename__ = 'Rooms'

    roomId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roomName = Column(Text, nullable=True)
    houseId = Column(UUID(as_uuid=True), ForeignKey(
        'House.houseId', ondelete='CASCADE'), nullable=False)
    createdAt = Column(DateTime(timezone=True),
                       server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relationships
    house: Mapped["Houses"] = relationship(
        "Houses", back_populates='rooms', cascade="all")
    devices: Mapped[List["Device"]] = relationship('Device',
                                                   cascade='all, delete-orphan')

    def get_data(self):
        room = RoomData()
        room.room_id = str(self.roomId)
        room.room_name = str(self.roomName)
        room.house_id = str(self.houseId)
        room.created_at = str(self.createdAt)
        room.updated_at = str(self.updatedAt)
        room.devices = [device.get_data() for device in self.devices]
        return room


class Device(Base):
    __tablename__ = 'Devices'

    deviceId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deviceName = Column(Text, nullable=False)
    pinNumber = Column(Integer, nullable=False, unique=True)
    status = Column(Boolean, default=False, nullable=False)
    isDefault = Column(Boolean, default=False, nullable=False)
    roomId = Column(UUID(as_uuid=True), ForeignKey(
        'Rooms.roomId', ondelete='CASCADE'), nullable=False)
    isScheduled = Column(Boolean, default=False, nullable=False)
    daysScheduled = Column(VARCHAR(30), nullable=True)
    startTime = Column(VARCHAR(10), nullable=True)
    offTime = Column(VARCHAR(10), nullable=True)
    scheduledBy = Column(Text, nullable=True)
    createdAt = Column(DateTime(timezone=True),
                       server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    def get_data(self):
        device = DeviceData()
        device.device_id = str(self.deviceId)
        device.device_name = str(self.deviceName)
        device.pin_number = int(str(self.pinNumber))
        device.status = bool(self.status)
        device.is_default = bool(self.isDefault)
        device.room_id = str(self.roomId)
        device.is_scheduled = bool(self.isScheduled)
        device.days_scheduled = str(
            self.daysScheduled) if self.daysScheduled is not None else None
        device.start_time = str(
            self.startTime)if self.startTime is not None else None
        device.off_time = str(
            self.offTime)if self.offTime is not None else None
        device.scheduled_by = str(
            self.scheduledBy)if self.scheduledBy is not None else None
        device.created_at = str(self.createdAt)
        device.updated_at = str(self.updatedAt)
        return device


class DeviceControlLog(Base):
    __tablename__ = "DeviceControlLogs"

    deviceControlLogId = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    statusChangedFrom = Column(Boolean, nullable=False)
    statusChangedTo = Column(Boolean, nullable=False)
    deviceId = Column(UUID(as_uuid=True), nullable=False)
    userId = Column(Text, nullable=False)
    createdAt = Column(DateTime(timezone=True),
                       server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    def get_data(self):
        device_control_log = DeviceControlLogData()
        device_control_log.device_control_log_id = str(self.deviceControlLogId)
        device_control_log.device_id = str(self.deviceId)
        device_control_log.user_id = str(self.userId)
        device_control_log.status_changed_from = bool(self.statusChangedFrom)
        device_control_log.status_changed_to = bool(self.statusChangedTo)
        device_control_log.created_at = str(self.createdAt)
        device_control_log.updated_at = str(self.updatedAt)
        return device_control_log
