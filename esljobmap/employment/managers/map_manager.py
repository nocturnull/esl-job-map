
from ..settings import *


class MapLocation:
    """GoogleMap location information wrapper."""
    zoom = 0
    lat = 0
    lng = 0

    def __init__(self, z, lt, lg):
        self.zoom = z
        self.lat = lt
        self.lng = lg


class MapManager:
    """GoogleMap location Manager"""

    @staticmethod
    def resolve_location_data(city_name: str) -> MapLocation:
        """
        Return a cities relevant google maps location information.

        :param city_name:
        :return:
        """
        if city_name == CITY_SEOUL:
            return MapLocation(13, 37.529451, 126.997417)
        elif city_name == CITY_BUSAN:
            return MapLocation(13, 35.1796, 129.0756)
        return MapLocation(8, 35.9078, 127.7669)
