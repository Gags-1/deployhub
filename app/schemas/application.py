from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    name: str
    repository: str
    environment: str


class ApplicationResponse(ApplicationCreate):
    id: int

    model_config= ConfigDict(from_attributes = True)
