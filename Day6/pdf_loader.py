from fastapi import UploadFile, File, HTTPException, status
import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY")
)

URL_ENDPOINT = os.environ.get("IMAGEKIT_URL_ENDPOINT")

async def upload_file(file: UploadFile = File(...)):
    try:

        file_data = await file.read()

        result = imagekit.upload(
            file=file_data,
            file_name=file.filename
        )
        
        return {"url": result.response_metadata.raw.get("url"), "fileId": result.response_metadata.raw.get("fileId")}
    except Exception as e:
        print("imagekit file uplaod error", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error uploading file")

async def delete_file(file_id: str):
    try:
        imagekit.delete_file(file_id)
    except Exception as e:
        print("imagekit file delete error", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting file")

