from fastapi import FastAPI,HTTPException, APIRouter, Depends
from enum import Enum
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import os

from config import settings

app=FastAPI(
    title="IDEF0 Generator",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO for developing. in production, replace with the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramVariantEnum(str, Enum):
    simple = "simple"
    complex = "complex"
    empty = "empty"

class DiagramQueryParams(BaseModel):
    variant: DiagramVariantEnum = Field(
        default=DiagramVariantEnum.simple,
        description="Type of the IDEF0 diagram to retrieve"
    )

router_v1 = APIRouter(prefix="/api/v1", tags=["Diagrams"])

@app.get("/health",tags=["System"])
def health_check():
    return {"status":"ok", "service":"IDEF0 Generator Backend"}

@router_v1.get("/diagram")
def get_diagram(params: Annotated[DiagramQueryParams, Depends()]):
    """
    It returns an XML file.
    The frontend will call this endpoint and receive the file contents.
    """
    filename=f"{params.variant.value}.xml"
    file_path=os.path.join(settings.DATA_DIR,filename)

    if os.path.exists(file_path):
        return FileResponse(file_path,media_type='application/xml',filename=filename)
    else:
        raise HTTPException(status_code=404,detail=f"Diagram '{filename}.xml' not found")
    
app.include_router(router_v1)