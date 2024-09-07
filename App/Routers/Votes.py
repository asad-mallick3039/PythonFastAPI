from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import Schemas, Models, Database, oAuth2 
from ..Database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags= ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Schemas.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oAuth2.get_current_user)):
    
    post_query = db.query(Models.Posts).filter(Models.Posts.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id:{vote.post_id} doesn't exist.")

    vote_query = db.query(Models.Votes).filter(
        Models.Votes.post_id == vote.post_id, Models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()

    if(vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail = f"User with id: {current_user.id} has already liked post {vote.post_id}")
        new_vote = Models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"Message": "Vote successfully cast."}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail = f"User with id: {current_user.id} has not liked post {vote.post_id}")
        
        vote_query.delete(syncronize_session= False)
        db.commit()

    return{"Message": "Vote removed from post."}