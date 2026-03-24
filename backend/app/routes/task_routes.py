from fastapi import APIRouter, HTTPException, status
from app.models.task import TaskCreate, TaskClassifyRequest, TaskClassifyResponse
from app.config.database import get_database
from app.services.ai_service import classify_task
from app.utils.xp_calculator import calculate_task_xp, distribute_xp, calculate_level
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter()


@router.post("/classify", response_model=dict)
async def classify_task_endpoint(request: TaskClassifyRequest):
    """Classify a task using AI"""
    classification = await classify_task(request.title)
    
    # Calculate XP based on classification
    xp_reward = calculate_task_xp(
        classification["difficulty"],
        classification["effort_score"]
    )
    
    classification["xpReward"] = xp_reward
    
    return {
        "success": True,
        "classification": classification
    }


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    db = get_database()
    
    # Calculate XP
    xp_reward = calculate_task_xp(task.difficulty.value, task.effortScore)
    
    # Create task document
    task_dict = task.model_dump()
    task_dict["xpReward"] = xp_reward
    task_dict["completed"] = False
    task_dict["completedAt"] = None
    task_dict["createdAt"] = datetime.utcnow()
    
    result = await db.tasks.insert_one(task_dict)
    
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    created_task["_id"] = str(created_task["_id"])
    
    return {
        "success": True,
        "task": created_task
    }


@router.get("/user/{user_id}", response_model=dict)
async def get_user_tasks(user_id: str, completed: Optional[bool] = None, limit: int = 50):
    """Get all tasks for a user"""
    db = get_database()
    
    query: dict = {"userId": user_id}
    if completed is not None:
        query["completed"] = completed
    
    tasks = await db.tasks.find(query).sort("createdAt", -1).limit(limit).to_list(length=limit)
    
    # Convert ObjectId to string
    for task in tasks:
        task["_id"] = str(task["_id"])
    
    return {
        "success": True,
        "count": len(tasks),
        "tasks": tasks
    }


@router.get("/user/{user_id}/today", response_model=dict)
async def get_today_tasks(user_id: str):
    """Get today's tasks for a user"""
    db = get_database()
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    tasks = await db.tasks.find({
        "userId": user_id,
        "createdAt": {"$gte": today, "$lt": tomorrow}
    }).sort("createdAt", -1).to_list(length=None)
    
    # Convert ObjectId to string
    for task in tasks:
        task["_id"] = str(task["_id"])
    
    completed = sum(1 for t in tasks if t["completed"])
    pending = sum(1 for t in tasks if not t["completed"])
    
    return {
        "success": True,
        "count": len(tasks),
        "completed": completed,
        "pending": pending,
        "tasks": tasks
    }


@router.get("/{task_id}", response_model=dict)
async def get_task(task_id: str):
    """Get a single task"""
    db = get_database()
    
    try:
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task["_id"] = str(task["_id"])
    
    return {
        "success": True,
        "task": task
    }


@router.put("/{task_id}", response_model=dict)
async def update_task(task_id: str, task_update: dict):
    """Update a task"""
    db = get_database()
    
    try:
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task["completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot edit completed task"
        )
    
    # Recalculate XP if difficulty or effort changed
    if "difficulty" in task_update or "effortScore" in task_update:
        difficulty = task_update.get("difficulty", task["difficulty"])
        effort_score = task_update.get("effortScore", task["effortScore"])
        task_update["xpReward"] = calculate_task_xp(difficulty, effort_score)
        
        if task.get("aiClassification"):
            task_update["aiClassification.wasEdited"] = True
    
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_update}
    )
    
    updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    updated_task["_id"] = str(updated_task["_id"])
    
    return {
        "success": True,
        "task": updated_task
    }


@router.post("/{task_id}/complete", response_model=dict)
async def complete_task(task_id: str):
    """Mark task as complete and award XP"""
    db = get_database()
    
    try:
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task["completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already completed"
        )
    
    # Mark task as completed
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"completed": True, "completedAt": datetime.utcnow()}}
    )
    
    # Get user
    user = await db.users.find_one({"_id": ObjectId(task["userId"])})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Calculate XP distribution
    xp_distribution = distribute_xp(
        task["xpReward"],
        task["primaryStat"],
        task.get("secondaryStat")
    )
    
    # Update user stats
    total_xp_gained = sum(xp_distribution.values())
    user["totalXP"] += total_xp_gained
    
    # Update global level
    global_level_info = calculate_level(user["totalXP"])
    user["level"] = global_level_info["level"]
    
    # Update individual stats
    for stat, xp in xp_distribution.items():
        user["stats"][stat]["xp"] += xp
        stat_level_info = calculate_level(user["stats"][stat]["xp"])
        user["stats"][stat]["level"] = stat_level_info["level"]
    
    # Update streak
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    last_completion = user["streak"].get("lastCompletionDate")
    
    if not last_completion:
        user["streak"]["current"] = 1
        user["streak"]["longest"] = 1
    else:
        last_date = last_completion.replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (today - last_date).days
        
        if days_diff == 0:
            pass  # Same day, no change
        elif days_diff == 1:
            user["streak"]["current"] += 1
            if user["streak"]["current"] > user["streak"]["longest"]:
                user["streak"]["longest"] = user["streak"]["current"]
        else:
            user["streak"]["current"] = 1
    
    user["streak"]["lastCompletionDate"] = today
    
    # Save user
    await db.users.update_one(
        {"_id": ObjectId(task["userId"])},
        {"$set": {
            "totalXP": user["totalXP"],
            "level": user["level"],
            "stats": user["stats"],
            "streak": user["streak"]
        }}
    )
    
    return {
        "success": True,
        "message": "Task completed successfully!",
        "xpGained": task["xpReward"],
        "xpDistribution": xp_distribution,
        "newLevel": user["level"],
        "streak": user["streak"]["current"]
    }


@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    """Delete a task"""
    db = get_database()
    
    try:
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID"
        )
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task["completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete completed task (it affects XP history)"
        )
    
    await db.tasks.delete_one({"_id": ObjectId(task_id)})
    
    return {
        "success": True,
        "message": "Task deleted successfully"
    }

# Made with Bob
