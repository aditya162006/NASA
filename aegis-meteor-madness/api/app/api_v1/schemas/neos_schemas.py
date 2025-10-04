from pydantic import BaseModel, Field
from typing import Optional


class EstimatedDiameter(BaseModel):
    min: float = Field(..., alias="min")
    max: float = Field(..., alias="max")


class NeoSummary(BaseModel):
    id: str
    name: str
    estimated_diameter_m: EstimatedDiameter
    close_approach_date: str


class NeoDetail(BaseModel):
    id: str
    name: str
    orbital_data: dict
    physical_data: dict
