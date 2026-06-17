from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi
from app.config.settings import settings
from typing import Optional

# MongoDB client instance
client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            server_api=ServerApi('1')
        )
        
        # Get database name from URI or use default
        database = client.get_database("levelup")
        
        # Test connection
        await client.admin.command('ping')
        print(f"✅ MongoDB Connected: {settings.MONGODB_URI.split('@')[1].split('/')[0]}")
        
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return database

