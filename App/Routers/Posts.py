from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import Models, Schemas, oAuth2
from ..Database import get_db

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"])


@router.get("/", response_model= List[Schemas.RespAfterVotes])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oAuth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = " "):
            #cursor.execute("""SELECT * FROM "Posts" """)
            #posts = cursor.fetchall()
    # To make all posts private: add the filter function:-
        #posts = db.query(Models.Posts).filter(
        #   Models.Posts.user_id == current_user.id).all() | else for public posts:
    #posts = db.query(Models.Posts).filter(
        #Models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(Models.Posts, func.count(Models.Votes.post_id).label("votes")).join(
        Models.Votes, Models.Votes.post_id == Models.Posts.id, isouter = True).group_by(Models.Posts.id).filter(
        Models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)  #Prints out the SQL Query for left outer join between Posts and Votes Tables.
    return (posts)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= Schemas.Response)
def create_posts(Post: Schemas.CreatePost, db: Session = Depends(get_db), 
                 current_user: int = Depends(oAuth2.get_current_user)):
    print(current_user)
            #post_dict = Post.dict()
            #post_dict['id'] = randrange(0, 1000000)
            #my_posts.append(post_dict)
            #cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
            #               (Post.title, Post.content, Post.published))
            #new_post= cursor.fetchone()
            #conn.commit()
        #new_post = Models.Post(title=Post.title, content= Post.content, published=Post.published) OR:
    new_post = Models.Posts(user_id = current_user.id, **Post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= Schemas.RespAfterVotes)
def get_posts(id: int, db: Session = Depends(get_db),
              current_user: int = Depends(oAuth2.get_current_user)):
    print(current_user)
            #cursor.execute("""SELECT * FROM "Posts" WHERE id = %s """, (str(id)))
            #post= cursor.fetchone()
    post = db.query(Models.Posts, func.count(Models.Votes.post_id).label("votes")).join(
        Models.Votes, Models.Votes.post_id == Models.Posts.id, isouter = True).group_by(Models.Posts.id).filter(
            Models.Posts.id == id).first()  
    #.all() not used because it will search for other matches after first match which will waste db resources.
    if not post:
            #response.status_code = status.HTTP_404_NOT_FOUND
            #return{"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} not found")
    
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oAuth2.get_current_user)):
    
    print(current_user)
            #index = find_index_posts(id)
            #cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (str(id)))
            #del_post= cursor.fetchone()
            #conn.commit()
    post_query = db.query(Models.Posts).filter(Models.Posts.id == id) 
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not Authorized to perform requested action.")
    
    post_query.delete()
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= Schemas.Response)
def update_post(id: int, Post :Schemas.PostDef, db: Session = Depends(get_db),
                current_user: int = Depends(oAuth2.get_current_user)):
    print(current_user)
            #cursor.execute("""UPDATE "Posts" SET title= %s, content= %s, published= %s WHERE id= %s RETURNING * """, 
            #               (Post.title, Post.content, Post.published, str(id)))
            #updated_post= cursor.fetchone()
            #conn.commit()
    post_query = db.query(Models.Posts).filter(Models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not Authorized to perform requested action.")
    
    post_query.update(Post.model_dump())
    db.commit()
    return post_query.first()