from enum import Enum
from typing import Annotated
from fastapi import FastAPI,HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import os

from config import get_settings
from schemas import SDiagramQueryParams

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


router_v1 = APIRouter(prefix="/api/v1", tags=["Diagrams"])

@app.get("/health",tags=["System"])
def health_check():
    return {"status":"ok", "service":"IDEF0 Generator Backend"}

@router_v1.get("/diagram")
def get_diagram(params: Annotated[SDiagramQueryParams, Depends()]):
    """
    It returns an XML file.
    The frontend will call this endpoint and receive the file contents.
    """
    filename=f"{params.variant.value}.xml"
    settings=get_settings()
    file_path=os.path.join(settings.DATA_DIR,filename)

    if os.path.exists(file_path):
        return FileResponse(file_path,media_type='application/xml',filename=filename)
    else:
        raise HTTPException(status_code=404,detail=f"Diagram '{filename}.xml' not found")
    
app.include_router(router_v1)
