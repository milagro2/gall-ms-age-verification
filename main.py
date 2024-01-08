import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()

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

        # Open the image and get its dimensions
        with Image.open(file_path) as img:
            width, height = img.size

        return JSONResponse(content={"width": width, "height": height}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {e}"}, status_code=500)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", default=8000)))
