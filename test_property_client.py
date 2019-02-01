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

    while prop.ws.sock.connected:
        for i in range(3):
            prop.set_value("wind_speed", 10 * i)
            time.sleep(5)
