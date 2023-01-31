from .. import utils, schemas, models, oauth2
from ..database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['auth'])

@router.post("/login")
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User Credential")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User Credential")
    
    #generate token
    #return token
    token = oauth2.create_access_token(data = {"user_id": user.id})
    #print(user.id)
    return {"access_token": token}
