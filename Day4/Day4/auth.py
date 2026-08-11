import os
from fastapi import HTTPException, Request, Depends
from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from sqlmodel import Session, select

from database import get_session
from models import Users

# Clerk client initialize karna
clerk = Clerk(
    bearer_auth=os.getenv("CLERK_SECRET_KEY")
)

# Authentication Dependency
def get_current_user(request: Request, db: Session = Depends(get_session)):
    try:
        # Clerk se token verify karna
        request_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5174"]
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated"
            )

        # Token se Clerk User ID nikalna
        clerk_user_id = request_state.payload["sub"]

        # Database mein us clerk id walay user ko dhoondna
        statement = select(Users).where(Users.clerk_user_id == clerk_user_id)
        user = db.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

# Authorization Dependency
def get_current_admin(user: Users = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user
