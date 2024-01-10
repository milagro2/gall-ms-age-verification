import os
from fastapi import FastAPI, UploadFile, File
import uvicorn
from deepface import DeepFace

app = FastAPI()

# Directory to store uploaded files
upload_dir = "uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{upload_dir}/{file.filename}"

    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # Use deepface to detect faces
    try:
        analysis = DeepFace.analyze(file_location)
        if analysis["region"] is not None:
            return {"message": "Face detected!"}
        else:
            return {"message": "No face detected."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
