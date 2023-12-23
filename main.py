# main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import PostgresUser
from database import mongodb_manager, database_manager, SessionLocal  # Import SessionLocal from database
from pydantic import BaseModel

app = FastAPI()

class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str

@app.post("/register")
async def register_user(user: UserRegistration):
    # Connect to MongoDB and PostgreSQL
    await mongodb_manager.connect()
    await database_manager.connect()

    try:
        # Create a PostgresUser instance without the profile_picture field
        db_user = PostgresUser(
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            phone=user.phone,
        )

        # Add user to PostgreSQL
        postgres_session = SessionLocal()
        if postgres_session.query(PostgresUser).filter_by(email=user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        postgres_session.add(db_user)
        postgres_session.commit()
        postgres_session.refresh(db_user)

        user_id = db_user.id

        # Handle profile picture in MongoDB
        profile_picture_data = {
            "user_id": user_id,
            "profile_picture": user.profile_picture,
        }
        await mongodb_manager.mongo_db.profile_pictures.insert_one(profile_picture_data)

        return {"message": "User registered successfully", "user_id": user_id}
    finally:
        # Disconnect from MongoDB and PostgreSQL
        await mongodb_manager.disconnect()
        await database_manager.disconnect()

@app.get("/user/{user_id}")
async def get_user_details(user_id: int):
    # Connect to MongoDB and PostgreSQL
    await mongodb_manager.connect()
    await database_manager.connect()

    try:
        # Fetch user details from PostgreSQL
        postgres_session = SessionLocal()
        db_user = postgres_session.query(PostgresUser).filter_by(id=user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch profile picture data from MongoDB
        profile_picture_data = await mongodb_manager.mongo_db.profile_pictures.find_one({"user_id": user_id})
        if not profile_picture_data:
            raise HTTPException(status_code=404, detail="Profile picture not found")

        user_details = {
            "id": db_user.id,
            "full_name": db_user.full_name,
            "email": db_user.email,
            "phone": db_user.phone,
            "profile_picture": profile_picture_data["profile_picture"],
        }

        return user_details
    finally:
        # Disconnect from MongoDB and PostgreSQL
        await mongodb_manager.disconnect()
        await database_manager.disconnect()
