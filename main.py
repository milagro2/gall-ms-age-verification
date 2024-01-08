import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

def get_image_dimensions(file_path):
    with open(file_path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
    
    return size

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

@app.post("/get_dimensions")
async def get_dimensions(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get the image dimensions
        size = get_image_dimensions(file_path)

        return JSONResponse(content={"size": size}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {e}"}, status_code=500)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", default=8000)))
