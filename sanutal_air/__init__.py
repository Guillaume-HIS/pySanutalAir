"""Library to handle communication with type D ventilation systems from Sanutal, AIR 2/3/4/5"""

import requests


class Ventilation(object):

    def __init__(self, host, name="Sanutal_Air"):
        self._name = name
        self._host = host
        self._state = None
        self._speed = None
        self._frost_active = None
        self._filter_reset = None
    
    def update(self):
        ret = requests.get("http://" + self._host + "/")
        self.fetch_speed(self, ret)
        self.fetch_frost_filter(self, ret)
    
    def fetch_speed(self, req_get):
        level = 0

        if "B1" in req_get.text[-130:]:
            level = 1
        if "B2" in req_get.text[-130:]:
            level = 2
        if "B3" in req_get.text[-130:]:
            level = 3
        if "B4" in req_get.text[-130:]:
            level = 4
        
        if level == 4 : return 100

        substring = f"document.getElementById(\"R{level}\").value="
        speed_index = req_get.text.rfind(substring)
        self._speed = int(req_get.text[len(substring) + speed_index : len(substring) + speed_index + 3].replace(";", "").replace("<", ""))

        if self._speed == 0:
            self._state = "on"
        else:
            self._state = "off"

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