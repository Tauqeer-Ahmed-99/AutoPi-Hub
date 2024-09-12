import os
import json

from database.actions import get_device_control_logs, get_house_data, get_house_members
from sqlalchemy.exc import SQLAlchemyError


# Ensure the directory exists
os.makedirs('data', exist_ok=True)


house_data = get_house_data()

if isinstance(house_data, SQLAlchemyError):
    raise Exception(house_data._message())

with open('data/house_data.json', 'w', encoding='utf-8') as f:
    json.dump(house_data.to_unsafe_dict(), f, ensure_ascii=False, indent=4)
    print("[Saved] House Data.")


house_members = get_house_members()

if isinstance(house_members, SQLAlchemyError):
    raise Exception(house_members._message())

with open('data/house_members.json', 'w', encoding='utf-8') as f:
    json.dump([house_member.to_dict()
              for house_member in house_members], f, ensure_ascii=False, indent=4)
    print("[Saved] House Members Data.")


logs = get_device_control_logs()

if isinstance(logs, SQLAlchemyError):
    raise Exception(logs._message())

with open('data/logs.json', 'w', encoding='utf-8') as f:
    json.dump([log.to_dict()
              for log in logs], f, ensure_ascii=False, indent=4)
    print("[Saved] Device Control Logs Data.")
