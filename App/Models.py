from  sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .Database import Base 

class Posts(Base):
    __tablename__ = "Posts"

    id        =Column(Integer, primary_key= True, nullable= False)
    title     =Column(String, nullable= False)
    content   =Column(String, nullable= False)
    published =Column(Boolean, server_default= 'TRUE', nullable= False)
    created_at=Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))
    user_id   =Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable= False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "Users"

    id        =Column(Integer, primary_key= True, nullable= False)
    email     =Column(String, nullable= False, unique= True)
    password  =Column(String, nullable= False)
    created_at=Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))

class Votes(Base):
   __tablename__ = "Votes"

   user_id = Column(Integer, ForeignKey(Users.id, ondelete="CASCADE"), primary_key= True)
   post_id = Column(Integer, ForeignKey(Posts.id, ondelete="CASCADE"), primary_key= True)
   