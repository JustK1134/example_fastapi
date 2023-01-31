from .. import utils, schemas, models, oauth2
from ..database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(tags=['Posts'])


@router.get("/")
def root():
    return {"message": "Hellow world"}


@router.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 2, search: Optional[str] = ""):
    #posts = cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    #post = cursor.fetchone()
    #conn.commit()
    post = models.Post(owner_id = user.id,**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post 
#title 

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this request")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"ID: {id} was not found"}
    
    return post

@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #delete_post = cursor.fetchone()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this request")
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} was not found")
    delete_post.delete()
    db.commit()
    #conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id =%s RETURNING *""", (new_post.title, new_post.content, new_post.published, str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this request")
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} was not found")
    post.update(new_post.dict(),synchronize_session=False)
    db.commit()
    #conn.commit()
    return post.first()