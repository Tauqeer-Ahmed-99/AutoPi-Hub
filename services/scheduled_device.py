from datetime import datetime


def get_scheduled_device_status(start_time: str, off_time: str) -> bool:
    current = datetime.now()
    current_time = current.hour * 60 + current.minute

    start_hour, start_minute = map(int, start_time.split(":"))
    off_hour, off_minute = map(int, off_time.split(":"))

    start_total_minutes = start_hour * 60 + start_minute
    off_total_minutes = off_hour * 60 + off_minute

    if start_total_minutes <= off_total_minutes:
        return start_total_minutes <= current_time <= off_total_minutes
    # Handle overnight case
    return current_time >= start_total_minutes or current_time <= off_total_minutes
