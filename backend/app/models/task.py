from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum


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


class StatType(str, Enum):
    """Available stat types"""
    strength = "strength"
    stamina = "stamina"
    mind = "mind"
    discipline = "discipline"
    selfCare = "selfCare"
    social = "social"


class DifficultyType(str, Enum):
    """Task difficulty levels"""
    easy = "easy"
    medium = "medium"
    hard = "hard"


class AIClassification(BaseModel):
    """AI classification metadata"""
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    wasEdited: bool = False


class TaskBase(BaseModel):
    """Base task model"""
    title: str
    description: Optional[str] = None
    primaryStat: StatType
    secondaryStat: Optional[StatType] = None
    difficulty: DifficultyType
    effortScore: int = Field(ge=1, le=10)
    dueDate: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Task creation model"""
    userId: str
    aiClassification: Optional[AIClassification] = None


class TaskInDB(TaskBase):
    """Task model as stored in database"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    userId: str
    xpReward: int
    completed: bool = False
    completedAt: Optional[datetime] = None
    aiClassification: Optional[AIClassification] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        use_enum_values = True


class TaskResponse(BaseModel):
    """Task response model"""
    id: str = Field(alias="_id")
    userId: str
    title: str
    description: Optional[str] = None
    primaryStat: str
    secondaryStat: Optional[str] = None
    difficulty: str
    effortScore: int
    xpReward: int
    completed: bool
    completedAt: Optional[datetime] = None
    dueDate: Optional[datetime] = None
    aiClassification: Optional[AIClassification] = None
    createdAt: datetime
    
    class Config:
        populate_by_name = True


class TaskClassifyRequest(BaseModel):
    """Request model for task classification"""
    title: str


class TaskClassifyResponse(BaseModel):
    """Response model for task classification"""
    primary_stat: str
    secondary_stat: Optional[str] = None
    difficulty: str
    effort_score: int
    reasoning: str
    confidence: float
    xpReward: int

# Made with Bob
