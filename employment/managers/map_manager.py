# employment/managers/map_manager.py

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
    def resolve_location_data(request, city_name: str) -> MapLocation:
        """
        Return a cities relevant google maps location information.

        :param request:
        :param city_name:
        :return:
        """

        if request.user_agent.is_pc:
            if city_name == CITY_SEOUL:
                return MapLocation(11, 37.529451, 126.997417)
            elif city_name == CITY_BUSAN:
                return MapLocation(12, 35.1796, 129.0756)
            return MapLocation(8, 36.5078, 127.7669)
        else:
            if city_name == CITY_SEOUL:
                return MapLocation(11, 37.529451, 126.997417)
            elif city_name == CITY_BUSAN:
                return MapLocation(12, 35.1496, 129.0756)
            return MapLocation(7, 36.5078, 127.7669)
