from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.config.database import connect_to_mongo, close_mongo_connection
from app.routes import user_routes, task_routes

app = FastAPI(
    title="LevelUp API",
    description="AI-Powered Gamified Life System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    await connect_to_mongo()
    print("🚀 LevelUp API started")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 API running on port {settings.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LevelUp API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "users": "/api/users",
            "tasks": "/api/tasks"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "LevelUp API is running",
        "environment": settings.ENVIRONMENT
    }


# Include routers
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(task_routes.router, prefix="/api/tasks", tags=["tasks"])

