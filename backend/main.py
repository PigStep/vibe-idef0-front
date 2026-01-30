import logging
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI,HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import get_settings
from schemas import SDiagramQueryParams


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
)
logger = logging.getLogger(__name__)

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
    logger.info("Requested diagram type: %s", params.variant.value)
    
    filename=f"{params.variant.value}.xml"
    settings=get_settings()

    base_path = Path(settings.DATA_DIR)
    file_path = base_path / filename


    if file_path.exists():
        return FileResponse(file_path,media_type='application/xml',filename=filename)
    else:
        error_msg = "Diagram %s not found in %s" % (filename,base_path)
        logger.error(error_msg)
        raise HTTPException(status_code=404,detail=error_msg)
    
app.include_router(router_v1)


