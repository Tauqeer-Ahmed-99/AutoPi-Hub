from datetime import datetime
from typing import List

from helpers.data_models import DeviceControlLog


def calculate_energy_consumption(logs: List[DeviceControlLog], end_date: datetime):
    '''Returns Energy Consumption in watt-hours'''
    total_energy_consumed = 0.0  # in watt-hours
    last_on_time = None

    # Iterate through logs to calculate total on-time
    for log in logs:
        if log.status_changed_to and not log.status_changed_from:
            # Device was turned ON
            last_on_time = datetime.fromisoformat(log.created_at)
        elif log.status_changed_from and not log.status_changed_to and last_on_time:
            # Device was turned OFF and there was a previous ON event
            duration = datetime.fromisoformat(
                log.created_at) - last_on_time  # timedelta
            hours_on = duration.total_seconds() / 3600  # Convert seconds to hours
            # Energy in watt-hours
            energy_consumed = (
                hours_on * log.device_wattage) if log.device_wattage is not None else 0.0
            total_energy_consumed += energy_consumed
            last_on_time = None  # Reset for the next on-off pair

    # Handle edge case where the device was still ON at the end of the period
    if last_on_time:
        duration = end_date - last_on_time
        hours_on = duration.total_seconds() / 3600
        energy_consumed = (
            hours_on * log.device_wattage) if log.device_wattage is not None else 0.0
        total_energy_consumed += energy_consumed

    return total_energy_consumed
