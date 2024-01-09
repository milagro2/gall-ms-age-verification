import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import face_recognition

app = FastAPI()

os.makedirs("uploads", exist_ok=True)

def get_image_dimensions(file_path: str):
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing image dimensions: {str(e)}")

def detect_faces(file_path: str):
    try:
        # Load the image file
        image = face_recognition.load_image_file(file_path)

        # Find all face locations in the image
        face_locations = face_recognition.face_locations(image)

        return face_locations
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error detecting faces: {str(e)}")

@app.post("/get_dimensions_and_faces/")
async def get_dimensions_and_faces(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Get image dimensions
        width, height = get_image_dimensions(file_path)

        # Detect faces
        face_locations = detect_faces(file_path)

        return {"filename": file.filename, "width": width, "height": height, "face_locations": face_locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", default=8000)))
