from fastapi import FastAPI

app = FastAPI(
    title="GroundTruth",
    description="Evidence-grounded AI biodiversity intelligence system",
    version="0.1.0"
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