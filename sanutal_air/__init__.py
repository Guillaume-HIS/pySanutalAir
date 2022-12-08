"""Library to handle communication with type D ventilation systems from Sanutal, AIR 2/3/4/5"""

import requests


class Ventilation(object):

    def __init__(self, host, name="Sanutal Air"):
        self._name = name
        self._host = host
        self._state = "unknown"
        self._speed = None
        self._level = None
        self._frost_active = None
        self._filter_reset = None
    
    def update(self):
        try:
            ret = requests.get("http://" + self._host + "/", timeout=5)
        except requests.Timeout:
            return 1
        if ret.status_code != 200:
            return 1
        self.fetch_speed(ret)
        self.fetch_frost_filter(ret)
        return 0
    
    def fetch_speed(self, req_get):
        self._level = 0

        if "B1" in req_get.text[-130:]:
            self._level = 1
        if "B2" in req_get.text[-130:]:
            self._level = 2
        if "B3" in req_get.text[-130:]:
            self._level = 3
        if "B4" in req_get.text[-130:]:
            self._level = 4
        
        if self._level == 4 :
            self._state = "on"
            self._speed = 100
            return

        substring = f"document.getElementById(\"R{self._level}\").value="
        speed_index = req_get.text.rfind(substring)
        self._speed = int(req_get.text[len(substring) + speed_index : len(substring) + speed_index + 3].replace(";", "").replace("<", ""))

        if self._speed == 0:
            self._state = "off"
        else:
            self._state = "on"

    def fetch_frost_filter(self, req_get):
        # Frost Active sensor
        substring = f"document.getElementById(\"D2\").style.backgroundColor=\""
        speed_index = req_get.text.rfind(substring)
        color_value = req_get.text[len(substring) + speed_index : len(substring) + speed_index + 7]
        if color_value == "#ffffff":
            self._frost_active = False
        else:
            self._frost_active = True
        
        # Filter Reset sensor
        substring = f"document.getElementById(\"D3\").style.backgroundColor=\""
        speed_index = req_get.text.rfind(substring)
        color_value = req_get.text[len(substring) + speed_index : len(substring) + speed_index + 7]
        if color_value == "#ffffff":
            self._filter_reset = False
        else:
            self._filter_reset = True

    def set_state_on(self):
        if self._state == "unknown":
            self.update()
        if self._state == "off":
            self.set_level(3)
            self._state = "on"
        self.update()

    def set_state_off(self):
        if self._state == "unknown":
            self.update()
        if self._state == "on":
            self.set_level(1)
            self._state = "off"
        self.update()

    def set_level(self, level):
        try:
            ret = requests.post("http://" + self._host + "/upload/B" + str(level), data="B" + str(level), timeout=5)
        except requests.Timeout:
            return 1
        if ret.status_code == 200:
            return 0
        else:
            return 1
    
    def set_l3_speed(self, speed):
        try:
            ret = requests.post("http://" + self._host + "/upload/R3" + str(speed), data="R3", timeout=5)
        except requests.Timeout:
            return 1
        if ret.status_code == 200:
            return 0
        else:
            return 1
    
    def set_speed(self, speed):
        """Set the speed of the fan, as a percentage."""
        if speed == 100:
            self.set_level(4)
            self.update()
            return
        self.set_l3_speed(speed)
        self.set_level(3)
        self.update()
    
    @property
    def name(self):
        return self._name
    
    @property
    def host(self):
        return self._host
    
    @property
    def state(self):
        return self._state
    
    @property
    def speed(self):
        return self._speed      

    @property
    def frost_active(self):
        return self._frost_active
    
    @property
    def filter_reset(self):
        return self._filter_reset