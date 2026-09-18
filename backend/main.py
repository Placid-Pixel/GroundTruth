from fastapi import FastAPI

from backend.models import (
    RecommendationRequest,
    RecommendationResponse,
)

from backend.graph import groundtruth_graph


app = FastAPI(
    title="GroundTruth",
    description="Evidence-grounded AI biodiversity intelligence system",
    version="0.3.0"
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
    result = groundtruth_graph.invoke(
        {
            "query": request.query,
            "environment": (
                request.environment.model_dump()
                if request.environment
                else None
            )
        }
    )

    return result["response"]