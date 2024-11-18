from pydantic import (
    BaseModel,
    Field,
)


class CoordinateSchema(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")


class CreateCircleSchema(BaseModel):
    coordinates: CoordinateSchema
    radius: float = Field(..., ge=1, description="Радиус окружности в метрах")
