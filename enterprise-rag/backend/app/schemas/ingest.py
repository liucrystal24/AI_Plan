from pydantic import BaseModel


class IngestRequest(BaseModel):
    path: str
    owner_dept: str = "public"
    visibility: str = "employee:all"
