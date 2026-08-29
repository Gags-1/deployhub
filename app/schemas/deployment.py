from pydantic import BaseModel, ConfigDict


class DeploymentCreate(BaseModel):
    application_id: int
    version: str
    commit_sha: str
    image: str
    environment: str


class DeploymentResponse(DeploymentCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
