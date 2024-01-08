from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
from typing import List

app = FastAPI()

# Create an 'uploads' directory to store the uploaded files
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

# Mount the 'uploads' directory as a static file directory
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Dictionary to store uploaded files information
uploaded_files = {}


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            file_path = upload_dir / unique_filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files[unique_filename] = file.filename

        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>Upload Successful</title>
            </head>
            <body>
                <h1>Upload Successful</h1>
                <p>Uploaded files:</p>
                <ul>
                    {"".join([f"<li>{filename}</li>" for filename in uploaded_files.values()])}
                </ul>
                <p><a href="/showfile">View Uploaded Files</a></p>
            </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>Error</title>
            </head>
            <body>
                <h1>Error Uploading Files: {e}</h1>
                <p><a href="/">Go back to home</a></p>
            </body>
        </html>
        """)


@app.get("/showfile", response_class=HTMLResponse, description="View all uploaded images.")
async def show_uploaded_files():
    images = []
    for display_filename in uploaded_files.values():
        images.append(f"<img src='/uploads/{display_filename}' style='max-width: 300px; max-height: 300px;'>")

    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Uploaded Images</title>
        </head>
        <body>
            <h1>Uploaded Images</h1>
            {''.join(images)}
            <p><a href="/">Go back to home</a></p>
        </body>
    </html>
    """)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
