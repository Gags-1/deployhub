from fastapi import FastAPI

app = FastAPI(
    title="DeployHub",
    description="Developer deployment platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to DeployHub",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/version")
def version():
    return {
        "version": "1.0.0",
    }
