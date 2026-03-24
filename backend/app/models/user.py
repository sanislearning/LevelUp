from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class StatData(BaseModel):
    """Individual stat data"""
    xp: int = 0
    level: int = 1


class Stats(BaseModel):
    """User stats"""
    strength: StatData = Field(default_factory=StatData)
    stamina: StatData = Field(default_factory=StatData)
    mind: StatData = Field(default_factory=StatData)
    discipline: StatData = Field(default_factory=StatData)
    selfCare: StatData = Field(default_factory=StatData)
    social: StatData = Field(default_factory=StatData)


class Streak(BaseModel):
    """Streak tracking"""
    current: int = 0
    longest: int = 0
    lastCompletionDate: Optional[datetime] = None


class UserBase(BaseModel):
    """Base user model"""
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation model"""
    pass


class UserInDB(UserBase):
    """User model as stored in database"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    totalXP: int = 0
    level: int = 1
    stats: Stats = Field(default_factory=Stats)
    streak: Streak = Field(default_factory=Streak)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponse(BaseModel):
    """User response model"""
    id: str = Field(alias="_id")
    name: str
    email: str
    totalXP: int
    level: int
    title: Optional[str] = None
    levelInfo: Optional[Dict] = None
    stats: Dict
    streak: Streak
    createdAt: datetime
    
    class Config:
        populate_by_name = True

# Made with Bob
