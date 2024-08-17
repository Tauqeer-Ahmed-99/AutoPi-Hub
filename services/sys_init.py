import bcrypt

from sqlalchemy.exc import SQLAlchemyError

from database.actions import get_house, init_house_db

from helpers.system_time import SystemTime


class SystemInitializer():

    sys_time: SystemTime

    def __init__(self) -> None:
        self.sys_time = SystemTime()
        self.initialize_house()

    def initialize_house(self):
        house = get_house()
        if isinstance(house, SQLAlchemyError):
            raise Exception("[House] Retrieve House failed.")
        if house is None:
            print("[House] House not initialized, initializing now...")
            house_password = self.get_house_password()
            hashed_pw = self.hash_password(house_password.strip())
            house = init_house_db(hashed_pw.decode("utf-8"))
            if isinstance(house, SQLAlchemyError):
                raise Exception(
                    f"[House] House Initialization failed. {house._message()}")
            print("[House] House Initialization Success.")
        else:
            print("[House] House Already Initialized. (Skipped)")

    def get_house_password(self):
        while True:
            house_password = input("Enter House Password: ")
            if len(house_password) >= 8:
                return house_password
            else:
                print("Password must be at least 8 characters long. Please try again.")

    def hash_password(self, password: str):
        salt = bcrypt.gensalt(10)
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pw

    def house_login(self, password: str):
        house = get_house()
        if isinstance(house, SQLAlchemyError):
            print(f"[House] House Login Error: {house._message()}")
            return None
        if house is None:
            print(f"[House] House is not initialized.")
            return None
        return bcrypt.checkpw(password.encode('utf-8'), house.house_password_hash.encode("utf-8"))
