from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   # has dictionary with 2 fields:
                                                                    #username and password.
from sqlalchemy.orm import Session
from .. import Database, Schemas, Models, Utils, oAuth2

router = APIRouter(
    tags=["Authentication"])

@router.post("/login", response_model= Schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Database.get_db)):
    user = db.query(Models.Users).filter(Models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials.")
    
    if not Utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials.")
    
    access_token = oAuth2.create_access_token(data = {"user_id":user.id})

    return{"access_token": access_token, "token_type": "bearer"}
