from fastapi import APIRouter, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.contact import (
    ContactMessage,
    ContactMessageCreate,
    ContactMessageResponse,
    ContactMessagesListResponse
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contact", tags=["contact"])


def get_db(request: Request) -> AsyncIOMotorDatabase:
    """Get database from app state"""
    return request.app.state.db


@router.post("", response_model=ContactMessageResponse, status_code=201)
async def create_contact_message(message_data: ContactMessageCreate, request: Request):
    """
    Create a new contact message
    
    - **name**: Sender's name (required, max 100 chars)
    - **email**: Sender's email (required, valid email format)
    - **subject**: Message subject (required, max 200 chars)
    - **message**: Message content (required, max 2000 chars)
    """
    try:
        db = get_db(request)
        
        # Get client info
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", None)
        
        # Create message object
        contact_message = ContactMessage(
            **message_data.dict(),
            timestamp=datetime.utcnow(),
            status="unread",
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        # Insert into database
        result = await db.contact_messages.insert_one(contact_message.dict())
        
        if result.inserted_id:
            logger.info(f"Contact message created: {contact_message.id} from {contact_message.email}")
            return ContactMessageResponse(
                success=True,
                message="Message sent successfully! I'll get back to you soon.",
                data=contact_message
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create message")
            
    except Exception as e:
        logger.error(f"Error creating contact message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("", response_model=ContactMessagesListResponse)
async def get_all_contact_messages(request: Request, limit: int = 100, skip: int = 0):
    """
    Get all contact messages (admin endpoint)
    
    - **limit**: Maximum number of messages to return (default: 100)
    - **skip**: Number of messages to skip (for pagination)
    """
    try:
        db = get_db(request)
        
        # Fetch messages sorted by timestamp (newest first)
        # Exclude MongoDB's _id field from results
        cursor = db.contact_messages.find({}, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit)
        messages = await cursor.to_list(length=limit)
        
        # Convert to ContactMessage objects
        contact_messages = [ContactMessage(**msg) for msg in messages]
        
        return ContactMessagesListResponse(
            success=True,
            count=len(contact_messages),
            data=contact_messages
        )
        
    except Exception as e:
        logger.error(f"Error fetching contact messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{message_id}", response_model=ContactMessageResponse)
async def get_contact_message(message_id: str, request: Request):
    """
    Get a specific contact message by ID
    
    - **message_id**: The unique ID of the message
    """
    try:
        db = get_db(request)
        
        # Find message by ID, exclude MongoDB's _id field
        message = await db.contact_messages.find_one({"id": message_id}, {"_id": 0})
        
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        contact_message = ContactMessage(**message)
        
        return ContactMessageResponse(
            success=True,
            message="Message retrieved successfully",
            data=contact_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contact message {message_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{message_id}")
async def delete_contact_message(message_id: str, request: Request):
    """
    Delete a contact message by ID (admin endpoint)
    
    - **message_id**: The unique ID of the message to delete
    """
    try:
        db = get_db(request)
        
        # Delete message
        result = await db.contact_messages.delete_one({"id": message_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        
        logger.info(f"Contact message deleted: {message_id}")
        
        return {
            "success": True,
            "message": "Message deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact message {message_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
