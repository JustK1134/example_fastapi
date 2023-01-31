from .. import utils, schemas, models, oauth2
from ..database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(tags=['vote'])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(post_vote: schemas.Vote, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_vote.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"POST_ID: {post_vote.id} was not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == post_vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()
    if (post_vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user.id} has already voted on post {post_vote.post_id}")
        new_vote =models.Vote(post_id = post_vote.post_id, user_id = user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully add vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully delete vote"}


@router.get("/vote")
def get_vote(db: Session = Depends(get_db)):
    vote = db.query(models.Vote).all()
    return {"vote": vote}
        