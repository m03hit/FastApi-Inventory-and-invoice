from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class MeasurementUnitEnum(str, Enum):
    sqfeet = "sqfeet"
    piece = "piece"


class MeasurementWay(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
