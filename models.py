# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

# Define the User model for PostgreSQL
class PostgresUser(Base):
    __tablename__ = "users"
    
    # Define columns
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)

# Define the ProfilePicture model for MongoDB
class ProfilePicture(Base):
    __tablename__ = "profile_pictures"
    
    # Define columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    picture_url = Column(String)

    # Define a relationship to PostgreSQL users
    user = relationship("PostgresUser", back_populates="profile_picture")

# Establish the reverse relationship in the User model
PostgresUser.profile_picture = relationship("ProfilePicture", back_populates="user")



