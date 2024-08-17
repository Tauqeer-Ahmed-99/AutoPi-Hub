import ntplib

from time import ctime
import datetime

import subprocess


class SystemTime():

    def __init__(self):
        self.set_system_time_from_server()

    def fetch_time_from_server(self):
        client = ntplib.NTPClient()
        try:
            # Replace 'pool.ntp.org' with your preferred NTP server
            response = client.request('pool.ntp.org', version=3)
            return datetime.datetime.strptime(ctime(response.tx_time), "%a %b %d %H:%M:%S %Y")
        except Exception as e:
            print(f"Failed to fetch time from NTP server: {e}")
            return None

    def set_system_time_from_server(self):
        server_time = self.fetch_time_from_server()
        if server_time:
            new_time = server_time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                # Run the 'date' command to set the system time
                subprocess.run(['sudo', 'date', '--set', new_time], check=True)
                print(f"System time set to {new_time}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to set system time: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Could not set system time because fetching time failed.")
