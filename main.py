import os
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

def get_image_dimensions(file_path: str):
    try:
        # Open the image using Pillow (PIL)
        from PIL import Image
        with Image.open(file_path) as img:
            # Get image dimensions
            width, height = img.size
            return width, height
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing image dimensions: {str(e)}")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Get image dimensions
        width, height = get_image_dimensions(file_path)

        return {"filename": file.filename, "width": width, "height": height}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello!"}

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))
