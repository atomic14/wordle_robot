import requests
from typing import Dict
import time


class PrinterAPI(object):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def connect(self):
        """Start connection to Duet"""
        url = f"{self.base_url}/rr_connect"
        r = requests.get(url, {"password": ""})
        if not r.ok:
            raise ValueError
        return r.json()

    def disconnect(self):
        """End connection to Duet"""
        url = f"{self.base_url}/rr_disconnect"
        r = requests.get(url)
        if not r.ok:
            raise ValueError
        return r.json()

    def is_homed(self) -> bool:
        """Is the printer homes?"""
        url = f"{self.base_url}/rr_model"
        r = requests.get(url, {"flags": "d99vn", "key": "move"})
        if not r.ok:
            raise ValueError
        result = r.json()["result"]
        return (
            result["axes"][0]["homed"]
            and result["axes"][1]["homed"]
            and result["axes"][2]["homed"]
        )

    def get_coords(self) -> Dict:
        """Get the current coordinates of the printer"""
        url = f"{self.base_url}/rr_model"
        r = requests.get(url, {"flags": "d99vn", "key": "move"})
        if not r.ok:
            raise ValueError
        result = r.json()["result"]
        return {
            result["axes"][0]["letter"]: result["axes"][0]["machinePosition"],
            result["axes"][1]["letter"]: result["axes"][1]["machinePosition"],
            result["axes"][2]["letter"]: result["axes"][2]["machinePosition"],
        }

    def send_code(self, code: str) -> Dict:
        """Send gcode to the printer"""
        url = f"{self.base_url}/rr_gcode"
        r = requests.get(url, {"gcode": code})
        if not r.ok:
            raise ValueError

    def home(self):
        """Home the axes"""
        self.send_code("G28")
        while not self.is_homed():
            time.sleep(0.5)

    def move(self, x=None, y=None, z=None, no_wait=False):
        """Move the printer to the given coordinates"""
        command = "G0 "
        if x is not None:
            command += f"X{x} "
        if y is not None:
            command += f"Y{y} "
        if z is not None:
            command += f"Z{z} "
        self.send_code(command + "F100000")
        if no_wait:
            return
        coords = self.get_coords()
        while (
            (x is not None and coords["X"] != x)
            or (y is not None and coords["Y"] != y)
            or (z is not None and coords["Z"] != z)
        ):
            time.sleep(0.05)
            coords = self.get_coords()

    def present_bed(self):
        self.move(x=0, y=228, no_wait=False)
