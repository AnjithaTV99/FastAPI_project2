# database.py

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from config import MONGODB_URL, DB_URL

# MongoDBManager for MongoDB connections
class MongoDBManager:
    def __init__(self, mongodb_url: str = MONGODB_URL):
        self.mongo_client = None
        self.mongo_db = None
        self.mongodb_url = mongodb_url

    async def connect(self):
        try:
            # Connect to the MongoDB server
            self.mongo_client = AsyncIOMotorClient(self.mongodb_url)
            # Access the "my_db" database
            self.mongo_db = self.mongo_client["my_db"]
        except Exception as e:
            # Handle connection error for MongoDB
            print(f"Error connecting to MongoDB: {e}")

    async def disconnect(self):
        try:
            # Disconnect from the MongoDB server
            if self.mongo_client:
                await self.mongo_client.close()
                print("Disconnected from MongoDB")
        except Exception as e:
            # Handle disconnection error for MongoDB
            print(f"Error disconnecting from MongoDB: {e}")

# Create an instance of MongoDBManager
mongodb_manager = MongoDBManager()


# SQLAlchemy model base
Base = declarative_base()

# Creating the SQLAlchemy engine and Database instance during initialization
engine = create_engine(DB_URL)
database = Database(DB_URL)

# Creating the SessionLocal class using sessionmaker and binding it to the SQLAlchemy engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self, db_url: str = DB_URL):
        self.engine = engine  # Use the pre-created engine
        self.database = database  # Use the pre-created database instance
        self.db_url = db_url

    async def connect(self):
        try:
            # Connect to the database
            await self.database.connect()
            print("Connected to the database")
        except Exception as e:
            # Log or handle the connection error appropriately
            print(f"Error connecting to the database: {e}")

    async def disconnect(self):
        try:
            # Disconnect from the database
            await self.database.disconnect()
            print("Disconnected from the database")
        except Exception as e:
            # Log or handle the disconnection error appropriately
            print(f"Error disconnecting from the database: {e}")

# Create an instance of DatabaseManager
database_manager = DatabaseManager()
