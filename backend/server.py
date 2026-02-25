from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone

# Import contact routes
from routes.contact import router as contact_router


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Charan's Portfolio API", version="1.0.0")

# Store db in app state for access in routes
app.state.db = db

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.get("/health")
async def health_check():
    """Health check endpoint to verify API and database connectivity"""
    try:
        # Test MongoDB connection
        await db.command("ping")
        return {
            "status": "healthy",
            "api": "running",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "api": "running",
            "database": "disconnected",
            "error": str(e)
        }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Include the router in the main app
app.include_router(api_router)

# Include contact router
app.include_router(contact_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_indexes():
    """Create MongoDB indexes on startup"""
    try:
        logger.info("=" * 50)
        logger.info("Starting Charan's Portfolio API")
        logger.info(f"Database: {os.environ.get('DB_NAME', 'test_database')}")
        logger.info(f"MongoDB URL: {mongo_url}")
        logger.info("=" * 50)
        
        # Test database connection
        await db.command("ping")
        logger.info("✓ MongoDB connection successful")
        
        # Create indexes for contact_messages collection
        await db.contact_messages.create_index("id", unique=True)
        await db.contact_messages.create_index("email")
        await db.contact_messages.create_index([("timestamp", -1)])  # Descending for sorting
        await db.contact_messages.create_index("status")
        logger.info("✓ MongoDB indexes created successfully")
        
        # Log available routes
        logger.info("✓ API Routes registered:")
        logger.info("  - GET  /api/")
        logger.info("  - GET  /api/health")
        logger.info("  - POST /api/contact")
        logger.info("  - GET  /api/contact")
        logger.info("  - GET  /api/contact/{id}")
        logger.info("  - DELETE /api/contact/{id}")
        logger.info("=" * 50)
        logger.info("Portfolio API is ready!")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        logger.warning("API may not function correctly")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()