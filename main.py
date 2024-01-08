from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
from typing import List
from PIL import Image
import cv2
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            file_path = upload_dir / unique_filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files[unique_filename] = file.filename

        return RedirectResponse(url="/showfile")
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
        
@app.get("/get_dimensions")
def read_hello():
    return {"message": "Bye Bye!"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
