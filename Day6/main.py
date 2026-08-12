from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session, select

from auth import get_current_user
from models import Users, Document
from database import create_db_and_tables, get_session
from schemas import UserSync
from pdf_loader import upload_file, delete_file


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/me")
def get_my_profile(current_user: Users = Depends(get_current_user)):
    return {
        "message": "Authenticate successful",
        "user_data": current_user
    }


@app.post("/sync-user")
def sync_user(user: UserSync, session: Session = Depends(get_session)):
    
    already_register = session.exec(select(Users).where(Users.clerk_user_id == user.clerk_user_id)).first()
    if already_register:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    new_user = Users(
        clerk_user_id = user.clerk_user_id,
        name = user.name,
        email = user.email,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "User Created Successfully", "user": new_user}

@app.post("/upload-document")
async def upload_document(file_uplaod: UploadFile = File(...), current_user: Users = Depends(get_current_user) , session: Session = Depends(get_session)):
    
    payload = await upload_file(file_uplaod)
    url = payload["url"]
    file_id = payload["fileId"]

    if not url or not file_id: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error uploading file")
    
    new_document = Document(
        user_id=current_user.id,
        file_url=url,
        imagekit_file_id=file_id,
    )

    session.add(new_document)
    session.commit()
    session.refresh(new_document)

    return {"message": "Document uploaded successfully", "data": new_document}

@app.delete("/delete-document")
async def delete_document(file_id: str, current_user: Users = Depends(get_current_user), session: Session = Depends(get_session)):
    
    if not file_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File id is required")
    
    document = session.exec(select(Document).where(Document.imagekit_file_id == file_id)).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    if document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this document")
    
    await delete_file(file_id)

    session.delete(document)
    session.commit()

    return {"message": "Document deleted successfully"}
