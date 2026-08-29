from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from app.database.connection import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.models.deployment import Deployment
from app.schemas.deployment import DeploymentCreate, DeploymentResponse


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

@app.post("/applications", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    db_application = Application(**application.model_dump())

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@app.get("/applications", response_model=list[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()


@app.post("/deployments", response_model=DeploymentResponse)
def create_deployment(
    deployment: DeploymentCreate,
    db: Session = Depends(get_db),
):
    db_deployment = Deployment(**deployment.model_dump())

    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)

    return db_deployment


@app.get("/deployments", response_model=list[DeploymentResponse])
def get_deployments(db: Session = Depends(get_db)):
    return db.query(Deployment).all()


@app.get("/deployments/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found",
        )

    return deployment

@app.patch("/deployments/{deployment_id}/status")
def update_deployment_status(
    deployment_id: int,
    status: str,
    db: Session = Depends(get_db),
):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found",
        )

    allowed_statuses = {
        "pending",
        "building",
        "deploying",
        "success",
        "failed",
    }

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {sorted(allowed_statuses)}",
        )

    deployment.status = status
    db.commit()
    db.refresh(deployment)

    return deployment
