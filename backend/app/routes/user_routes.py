from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserResponse, UserInDB, Stats
from app.config.database import get_database
from app.utils.xp_calculator import calculate_level, get_title
from bson import ObjectId
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Create user document
    user_dict = user.model_dump()
    user_dict["totalXP"] = 0
    user_dict["level"] = 1
    user_dict["stats"] = Stats().model_dump()
    user_dict["streak"] = {"current": 0, "longest": 0, "lastCompletionDate": None}
    user_dict["createdAt"] = datetime.utcnow()
    
    result = await db.users.insert_one(user_dict)
    
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    
    return {
        "success": True,
        "user": {
            "id": created_user["_id"],
            "name": created_user["name"],
            "email": created_user["email"],
            "level": created_user["level"],
            "totalXP": created_user["totalXP"],
            "stats": created_user["stats"],
            "streak": created_user["streak"]
        }
    }


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str):
    """Get user profile with detailed stats"""
    db = get_database()
    
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Calculate level info for global level
    global_level_info = calculate_level(user["totalXP"])
    
    # Calculate level info for each stat
    stats_with_level_info = {}
    for stat_name, stat_data in user["stats"].items():
        stat_level_info = calculate_level(stat_data["xp"])
        stats_with_level_info[stat_name] = {
            "xp": stat_data["xp"],
            "level": stat_data["level"],
            "currentLevelXP": stat_level_info["currentLevelXP"],
            "xpForNextLevel": stat_level_info["xpForNextLevel"],
            "progress": stat_level_info["progress"]
        }
    
    return {
        "success": True,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "totalXP": user["totalXP"],
            "level": user["level"],
            "title": get_title(user["level"]),
            "levelInfo": global_level_info,
            "stats": stats_with_level_info,
            "streak": user["streak"],
            "createdAt": user["createdAt"]
        }
    }


@router.get("/{user_id}/stats", response_model=dict)
async def get_user_stats(user_id: str):
    """Get user stats summary"""
    db = get_database()
    
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    stats_array = []
    for name, data in user["stats"].items():
        level_info = calculate_level(data["xp"])
        stats_array.append({
            "name": name,
            "xp": data["xp"],
            "level": data["level"],
            "progress": level_info["progress"]
        })
    
    # Sort by level descending
    stats_array.sort(key=lambda x: x["level"], reverse=True)
    
    return {
        "success": True,
        "stats": stats_array,
        "totalXP": user["totalXP"],
        "globalLevel": user["level"],
        "title": get_title(user["level"])
    }


@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, name: str = None):
    """Update user profile"""
    db = get_database()
    
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = {}
    if name:
        update_data["name"] = name
    
    if update_data:
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    return {
        "success": True,
        "user": {
            "id": str(updated_user["_id"]),
            "name": updated_user["name"],
            "email": updated_user["email"]
        }
    }

# Made with Bob
