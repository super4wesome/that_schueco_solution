from __future__ import print_function

import json
import threading
import time
import pprint

# pip install websocket-client
# !! NOT: pip install websocket
import websocket

CONNECTION_REQUEST = {
    "type": "connection_request",
    "request_type": "connect_to_prop",
    "prop_id": 0
}

SET_VALUE = {
    "type": "set_value",
    "value_name": "ambient_temperature",
    "value": 10.0
}


class PropertyClient(object):
    def __init__(self, url, prop_id=0):
        self.prop_id = prop_id
        self.data = {}
        self.ws = websocket.WebSocketApp(
            url,
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws))
        # Start run_forever() asynchronously to be non-blocking.
        self.run_thread = threading.Thread(target=self.ws.run_forever)
        self.run_thread.daemon = True
        self.run_thread.start()

    def wait_until_connected(self, timeout=5):
        # Stupid but YOLO
        while not self.ws.sock.connected and timeout:
            time.sleep(1)
            timeout -= 1

    def is_connected(self):
        return self.ws.sock.connected

    def spin(self):
        try:
            while self.run_thread.is_alive():
                self.run_thread.join(1)
        except KeyboardInterrupt:
            pass

    def on_message(self, ws, message):
        payload = json.loads(message)
        if payload["type"] == "property_update":
            self.data.update({payload["value_name"]: payload["value"]})
        print(payload["value_name"], "was set to", payload["value"])

    def on_error(self, ws, error):
        print("ERROR:", error)

    def on_close(self, ws):
        print("Socket closed!")

    def on_open(self, ws):
        def run(*args):
            request = CONNECTION_REQUEST
            request["prop_id"] = self.prop_id
            self.ws.send(json.dumps(request))

        thread = threading.Thread(target=run)
        thread.start()

    def set_value(self, value_name, value):
        request = SET_VALUE
        request["value_name"] = value_name
        request["value"] = value
        print("Sending request to update", request["value_name"], "to",
              request["value"])
        self.ws.send(json.dumps(request))

    def get_value(self, value_name):
        return self.data[value_name]
