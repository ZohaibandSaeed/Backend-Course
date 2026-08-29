from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session, create_tables
from imagekit import upload_file, delete_file
from models import FileModel
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/upload_file")
async def upload_file_route(file: UploadFile = File(...), session: Session = Depends(get_session)):

    if not file:
        raise HTTPException(status_code = 400, detail="No file provided")
    
    file_upload = await upload_file(file, file.filename)

    file_model = FileModel(
        imagekit_id = file_upload["file_id"],
        file_url = file_upload["file_url"]
    )

    session.add(file_model)
    session.commit()
    session.refresh(file_model)
    
    return f"File Upload Successfully {file_upload}"
    

@app.delete("/delete_file")
def delete_file_route(payload: str, session: Session = Depends(get_session)):

    if not payload:
        raise HTTPException(status_code=400, detail="Please provide imagekit_id")
    
    file_in_db = session.exec(select(FileModel).where(FileModel.imagekit_id == payload)).first()

    if not file_in_db:
        raise HTTPException(status_code=400, detail="No file found")
    
    response = delete_file(payload)
    print(response)

    session.delete(file_in_db)
    session.commit()

    return {"message": "File deleted successfully"}


