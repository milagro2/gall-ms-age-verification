import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from PIL import Image

app = FastAPI()

upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
    
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    dimensions = get_image_dimensions(file_path)

    return {"filename": file.filename, "dimensions": dimensions}


def get_image_dimensions(image_path: Path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return {"width": width, "height": height}
    except Exception as e:
        return {"error": f"Unable to get dimensions: {e}"}

@app.get("/get_dimensions")
def read_hello():
    return {"message": "Bye Bye!"}

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))
