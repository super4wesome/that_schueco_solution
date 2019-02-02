from __future__ import print_function

import csv
from dateutil import parser
import datetime
import os
import time

from property_client import PropertyClient

URL = "ws://schuecobe5hackdays.azurewebsites.net/WebSocketServer.ashx?"
HERE = os.path.dirname(os.path.realpath(__file__))
DATASET_PATH = os.path.join(HERE, "datasets/jena_climate_2009_2016.csv")


if __name__ == "__main__":
    prop = PropertyClient(URL, prop_id=666)
    prop.wait_until_connected(timeout=10)

    with open(DATASET_PATH) as dataset:
        reader = csv.reader(dataset)
        header = next(reader)
        print(header)
        for row in reader:
            date_time_str = row[0]
            date_time = parser.parse(date_time_str, dayfirst=True)
            if date_time < parser.parse("01.04.2009 00:00:00", dayfirst=True):
                # skip boring winter
                continue
            temp = row[2]
            atmospheric_pressure = float(row[1])
            relative_humidity = float(row[5])
            wind_direction = row[14]
            wind_speed = row[12]
            prop.set_value("wind_speed", wind_speed)
            prop.set_value("wind_direction", wind_direction)
            prop.set_value("userdefined_string_1", date_time_str)
            prop.set_value("ambient_temperature", temp)
            if 21 < date_time.hour or date_time.hour < 6:
                prop.set_value("sun_state", "Dark")
            # Approximately the mean of the dataset.
            elif atmospheric_pressure > 990 and relative_humidity < 65:
                prop.set_value("sun_state", "Sunny")
            else:
                prop.set_value("sun_state", "Cloudy")
            time.sleep(0.5)
