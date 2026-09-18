from typing import List, Optional
from pydantic import BaseModel, Field


class EnvironmentalInput(BaseModel):
    soil_organic_carbon: Optional[float] = Field(
        default=None,
        description="Soil organic carbon percentage"
    )

    soil_ph: Optional[float] = Field(
        default=None,
        description="Soil pH"
    )

    soil_moisture: Optional[float] = Field(
        default=None,
        description="Soil moisture percentage"
    )

    biodiversity: Optional[float] = Field(
        default=None,
        description="Biodiversity indicator or index"
    )

    water_availability: Optional[float] = Field(
        default=None,
        description="Water availability indicator"
    )

    land_use: Optional[str] = Field(
        default=None,
        description="Current land-use type"
    )

    pollution: Optional[float] = Field(
        default=None,
        description="Pollution indicator"
    )


class RecommendationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Natural-language environmental question"
    )

    environment: Optional[EnvironmentalInput] = None


class EvidenceItem(BaseModel):
    id: str
    source: str
    year: int
    title: str
    supporting_metrics: List[str]
    similarity_score: Optional[float] = None
    evidence_score: Optional[float] = None


class Recommendation(BaseModel):
    action: str
    reasoning: str
    metrics_impacted: List[str]
    time_horizon: str
    evidence: List[EvidenceItem]


class RecommendationResponse(BaseModel):
    query: str
    findings: List[dict] = []
    recommendations: List[Recommendation] = []