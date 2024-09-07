from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import Models, Schemas, Utils
from sqlalchemy.orm import Session
from ..Database import get_db

router = APIRouter(
    prefix="/users",
    tags= ["Users"])


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=Schemas.RespToUser)
def create_user(user: Schemas.User, db: Session = Depends(get_db)):

    hashed_password = Utils.hash(user.password)
    user.password = hashed_password            
    #hashing the user input password using bcrypt module from passlib library

    new_user = Models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=Schemas.RespToUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Models.Users).filter(Models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} doesn't exist.")
    return user
    