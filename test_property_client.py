from __future__ import print_function

import time

# pip install websocket-client
# !! NOT: pip install websocket
import websocket

from property_client import PropertyClient


URL = "ws://schuecobe5hackdays.azurewebsites.net/WebSocketServer.ashx?"


if __name__ == '__main__':
    # For debugging.
    # websocket.enableTrace(True)

    # ID 0 would auto-assign a new number, we use 666 ;)
    prop = PropertyClient(URL, prop_id=666)
    prop.wait_until_connected(timeout=10)

    i = 0
    while prop.is_connected() and i <= 3:
        prop.set_value("wind_speed", 10 * i)
        print("Checking value for ambient temperature:",
              prop.get_value("ambient_temperature"))
        time.sleep(2)
        i += 1

    def custom_callback(value):
        print("Custom callback received:", value)

    def other_custom_callback(value):
        print("Other custom callback received:", value)

    prop.add_callback("ambient_temperature", custom_callback)
    prop.add_callback("ambient_temperature", other_custom_callback)

    print("Going into passive spin mode, only receiving values...")
    prop.spin()
