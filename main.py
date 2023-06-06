from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Enum as EnumSQL, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLAlchemy models

Base = declarative_base()


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(EnumSQL(GenderEnum))


# Create the FastAPI app

app = FastAPI()

# SQLAlchemy setup

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Pydantic model for user creation

class UserCreate(BaseModel):
    name: str
    gender: GenderEnum


# API endpoint to create a user

@app.post("/users")
def create_user(user: UserCreate):
    user_to_add = User(name=user.name, gender=user.gender)
    session.add(user_to_add)
    session.commit()
    return {"message": "User created successfully"}


# Run the FastAPI application

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
