from enum import Enum


class CoordinateReferenceSystemEnum(str, Enum):
    WGS_84 = "WGS_84"

    @property
    def srid(self):
        systems = {self.WGS_84: 4326}

        return systems.get(self)
