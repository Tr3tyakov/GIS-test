from pydantic import BaseModel


class CoordinateSchema(BaseModel):
    longitude: float
    latitude: float



class CreateCircleSchema(BaseModel):
    coordinates: CoordinateSchema
    radius: float