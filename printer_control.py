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

    def move(self, x, y, z):
        """Move the printer to the given coordinates"""
        self.send_code(f"G0 X{x} Y{y} Z{z}")
        coords = self.get_coords()
        while coords["X"] != x or coords["Y"] != y or coords["Z"] != z:
            time.sleep(0.1)
            coords = self.get_coords()
