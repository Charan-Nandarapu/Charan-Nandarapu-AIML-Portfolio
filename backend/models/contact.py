from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class ContactMessageCreate(BaseModel):
    """Schema for creating a new contact message"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)


class ContactMessage(BaseModel):
    """Schema for contact message response"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    subject: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="unread")
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContactMessageResponse(BaseModel):
    """API response schema for contact message"""
    success: bool
    message: str
    data: Optional[ContactMessage] = None


class ContactMessagesListResponse(BaseModel):
    """API response schema for list of contact messages"""
    success: bool
    count: int
    data: list[ContactMessage]
