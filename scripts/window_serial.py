#! /usr/bin/python

import serial
import time
import websocket
from property_client import PropertyClient


class SchuecoConnection:
    def __init__(self):
        # TODO: udev-rule
        self.connected = False
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)
            self.connected = True
        except serial.SerialException as e:
            print(e)
            return

        # print("Connection established")

    def move_window(self, state):
        assert self.connected
        assert state in ['Closed', 'Tilt', 'Turned']
        msg = None
        if state == 'Closed':
            msg = serial.to_bytes([0x04, 0x23, 0x30, 0x40, 0x01, 0x01, 0x03, 0x64, 0x09, 0x00])
        if state == 'Turned':
            msg = serial.to_bytes([0x05, 0x23, 0x30, 0x40, 0x32, 0x01, 0x03, 0x64, 0xD7, 0x00])
        if state == 'Tilt':
            msg = serial.to_bytes([0x05, 0x23, 0x30, 0x40, 0x64, 0x01, 0x03, 0x64, 0xA5, 0x00])

        self.ser.write(msg)
        sc._read_message()  # get immediate feedback and ignore it

    def get_window_state(self):
        assert self.connected
        self.ser.write(serial.to_bytes([0x05, 0x22, 0x30, 0x70, 0x3E, 0x00]))
        msg = self._read_message()
        return self._parse_window_state(msg)

    def get_temperatures(self):
        assert self.connected
        get_sensor = serial.to_bytes([0x05, 0x22, 0x06, 0xB1, 0x27, 0x00])
        self.ser.write(get_sensor)
        msg = self._read_message()
        return self._parse_temperature(msg)

    def _parse_window_state(self, msg):
        assert (len(msg) == 9)
        return msg[7]

    def _read_message(self):
        msg = []
        nid = -1
        while True:
            byte = ord(self.ser.read(1))
            if nid == -1:
                nid = byte
                continue
            nid -= 1
            if nid == 0:
                if byte == 0:
                    break
                else:
                    nid = byte
                    msg.append(0)
            else:
                msg.append(byte)
        return msg

    def _parse_temperature(self, msg):
        assert len(msg) == 18
        a = msg[6]
        b = msg[7]
        t1 = ((b*16*16 + a)/10.0-273)

        a = msg[9]
        b = msg[10]
        t2 = ((b*16*16 + a)/10.0-273)

        s1 = "%.2f" % t1
        s2 = "%.2f" % t2
        return [s1, s2]

    def window_state_callback(self, data):
        print(data)
        self.move_window(data)


if __name__ == '__main__':
    sc = SchuecoConnection()
    print("Temperatures: %s" % str(sc.get_temperatures()))
    print("Window state: %i %% " % sc.get_window_state())
    # sc.move_window('close')

    URL = "ws://schuecobe5hackdays.azurewebsites.net/WebSocketServer.ashx?"
    prop = PropertyClient(URL, prop_id=666)
    prop.wait_until_connected(timeout=10)
    prop.add_callback("room2nd_window_state", sc.window_state_callback)

    while prop.is_connected():
        t1, t2 = sc.get_temperatures()
        prop.set_value('room2nd_temperature', t1)
        prop.set_value('room4th_temperature', t2)

        time.sleep(5)

    print("Terminating")





