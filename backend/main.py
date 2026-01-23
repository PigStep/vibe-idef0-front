from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app=FastAPI()

# This allows the frontend (which runs, for example, on port 3000)
# to make requests to your server on port 8000. 
# Without this, the browser will block the request.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # for developing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR="data"

@app.get("/")
def read_root():
    return {"status":"ok","message":"Backend is running!", "service":"IDEF0 Generator Backend"}

@app.get("/api/get-diagram")
def get_diagram(variant:str="simple"):
    """It returns an XML file.
    The frontend will call this endpoint and receive the file contents.
    """
    filename=f"{variant}.xml"
    file_path=os.path.join(DATA_DIR,filename)

    if os.path.exists(file_path):
        return FileResponse(file_path,media_type='application/xml',filename=filename)
    else:
        raise HTTPException(status_code=404,detail=f"Diagram '{filename}.xml' not found")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)

