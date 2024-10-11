from pydantic import BaseModel


class AddRoomRequest(BaseModel):
    userId: str
    userName: str
    houseId: str
    roomName: str


class RemoveRoomRequest(BaseModel):
    userId: str
    userName: str
    houseId: str
    roomId: str
    roomName: str


class AddDeviceRequest(BaseModel):
    houseId: str
    userId: str
    userName: str
    roomId: str
    pinNumber: int
    deviceName: str
    wattage: float


class SwitchDeviceRequest(BaseModel):
    houseId: str
    userId: str
    userName: str
    deviceId: str
    deviceName: str
    statusFrom: bool
    statusTo: bool


class ConfigureDeviceRequest(BaseModel):
    houseId: str
    userId: str
    userName: str
    deviceId: str
    deviceName: str
    pinNumber: int
    status: bool
    isDefault: bool
    isScheduled: bool
    daysScheduled: str
    startTime: str
    offTime: str
    wattage: float


class RemoveDeviceRequest(BaseModel):
    userId: str
    userName: str
    houseId: str
    roomId: str
    deviceId: str
    deviceName: str


class ResponseStatusCodes():
    INVALID_DATA = "INVALID_DATA"
    HOUSE_NOT_INITIALIZED = "HOUSE_NOT_INITIALIZED"
    INVALID_CREDS = "INVALID_CREDS"
    SERVER_ERROR = "SERVER_ERROR"
    USER_LOGGEDIN = "USER_LOGGEDIN"
    INVALID_REQUEST = "INVALID_REQUEST"
    REQUEST_FULLFILLED = "REQUEST_FULLFILLED"
    SWITCH_DEVICE_ERROR = "SWITCH_DEVICE_ERROR"


def is_valid_request(request_body: list):
    for item in request_body:
        if item is None:
            return False
    return True
