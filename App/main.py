from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import Models
from .Database import engine
from .Routers import Posts, Users, Auth, Votes




# Models.Base.metadata.create_all(bind=engine) :- Tells sqlalchemy to execute all its create stmts 
                                             #   that creates new tables automatically.

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

    #used when postgresql was not used:
    #def find_post(id):
    #   for p in my_posts:
    #        if p['id'] == id:
    #            return p
            
    #def find_index_posts(id):
    #    for i,p in enumerate(my_posts):
    #       if p['id'] == id:
    #            return i
        
app.include_router(Posts.router)
app.include_router(Users.router)
app.include_router(Auth.router)
app.include_router(Votes.router)
    
@app.get("/")
def root():
    return{"Message":"Hello World."}

