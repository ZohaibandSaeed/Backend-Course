from importlib.metadata import files
from fastapi import HTTPException
import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY")
)

URL_ENDPOINT = os.getenv("IMAGEKIT_ENDPOINT_URL")

async def upload_file(file, file_id):
    try:
        file_bytes = await file.read()
        response = imagekit.files.upload(
            file = file_bytes,
            file_name = file_id,
            folder="/files"
        )

        return {
            "file_id": response.fileId,
            "file_url": response.url
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_file(imagekit_id):
    try:
        response = imagekit.files.delete(
            file_id = imagekit_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File not deleted {e}")
