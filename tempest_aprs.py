import socket
import json
from datetime import datetime
import os
import pytz

# Specify the time zone you want to use as an offset
local_timezone = pytz.timezone("US/Arizona")  # Change this to your desired time zone

UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 50222  # Replace with the correct UDP port for WeatherFlow

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    decoded_data = data.decode('utf-8')

    try:
        # Parse the JSON data
        observation = json.loads(decoded_data)

        # Check if it's an observation with the type "obs_st"
        if observation.get("type") == "obs_st":
            obs_data = observation.get("obs")

            # Check if the observation data is non-empty and has enough values
            if obs_data and len(obs_data[0]) >= 17:
                time_epoch, wind_avg, wind_dir, air_temp, station_pressure = obs_data[0][0], obs_data[0][2], obs_data[0][4], obs_data[0][7], obs_data[0][6]

                # Convert the epoch time to local time with the specified time zone
                utc_time = datetime.utcfromtimestamp(time_epoch)
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

                # Convert units (if needed) and round to two decimal places
                wind_speed_mph = round(wind_avg * 2.23694, 2)  # m/s to mph
                air_temp_fahrenheit = round((air_temp * 9/5) + 32, 2)  # Celsius to Fahrenheit
                station_pressure_mb = round(station_pressure, 2)

                # Construct an APRS message format
                aprs_message = f">WX Beacon: {local_time.strftime('%Y-%m-%d %H:%M:%S')}, Wind: {wind_speed_mph}mph {wind_dir}°, Temp: {air_temp_fahrenheit}°F, Pressure: {station_pressure_mb}mb"

                # Delete the existing file, if it exists
                if os.path.exists('/tmp/wxbeacon.txt'):
                    os.remove('/tmp/wxbeacon.txt')

                # Create a new file and write the APRS message to it
                with open('/tmp/wxbeacon.txt', 'w') as file:
                    file.write(aprs_message)

    except json.JSONDecodeError:
        pass
