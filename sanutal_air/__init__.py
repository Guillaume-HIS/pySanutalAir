"""Library to handle communication with type D ventilation systems from Sanutal, AIR 2/3/4/5"""

import requests


class Ventilation(object):

    def __init__(self, host, name="Sanutal_Air"):
        self._name = name
        self._host = host
        self._is_on = None
        self._speed = None
        self._frost_active = None
        self._filter_reset = None