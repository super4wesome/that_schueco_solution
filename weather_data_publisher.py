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
        i = 0
        for row in reader:
            # i += 1
            # if i % 60 != 0:
            #     continue
            date_time_str = row[0]
            date_time = parser.parse(date_time_str)
            temp = row[2]
            atmospheric_pressure = float(row[1])
            wind_direction = row[14]
            wind_speed = row[12]
            prop.set_value("wind_speed", wind_speed)
            prop.set_value("wind_direction", wind_direction)
            prop.set_value("userdefined_string_1", date_time_str)
            prop.set_value("ambient_temperature", temp)
            print(date_time.hour)
            if 21 < date_time.hour or date_time.hour < 6:
                prop.set_value("sun_state", "Dark")
            # Approximately the mean of the dataset.
            elif atmospheric_pressure > 990:
                prop.set_value("sun_state", "Sunny")
            else:
                prop.set_value("sun_state", "Cloudy")
            time.sleep(0.05)
