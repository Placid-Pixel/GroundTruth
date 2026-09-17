from fastapi import FastAPI

from backend.models import (
    RecommendationRequest,
    RecommendationResponse,
)

from backend.semantic_retriever import retriever
from backend.reasoning import analyze_environment
from backend.recommendation import ground_recommendations


app = FastAPI(
    title="GroundTruth",
    description="Evidence-grounded AI biodiversity intelligence system",
    version="0.2.0"
)


@app.get("/")
def root():
    return {
        "message": "GroundTruth API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend(
    request: RecommendationRequest
):
    # 1. Retrieve scientific evidence
    evidence = retriever.retrieve(
        request.query,
        top_k=5
    )

    # 2. Extract structured environmental variables
    environment = request.environment

    if environment:
        analysis = analyze_environment(
            soil_organic_carbon=environment.soil_organic_carbon,
            soil_ph=environment.soil_ph,
            soil_moisture=environment.soil_moisture,
            biodiversity=environment.biodiversity,
            water_availability=environment.water_availability,
            land_use=environment.land_use,
            pollution=environment.pollution,
        )
    else:
        analysis = {
            "findings": [],
            "recommendations": []
        }

    # 3. Ground recommendations with retrieved evidence
    grounded = ground_recommendations(
        analysis["recommendations"],
        evidence
    )

    return {
        "query": request.query,
        "findings": analysis["findings"],
        "recommendations": grounded
    }