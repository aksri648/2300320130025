from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Pydantic Models
class Notification(BaseModel):
    id: str
    type: str
    title: str
    message: str
    priority: str
    isRead: bool
    createdAt: datetime
    readAt: Optional[datetime] = None
    actionUrl: str
    metadata: Optional[dict] = None

class NotificationsResponse(BaseModel):
    page: int
    size: int
    totalElements: int
    totalPages: int
    notifications: List[Notification]

class UnreadCountResponse(BaseModel):
    unreadCount: int

class MarkAsReadRequest(BaseModel):
    isRead: bool

class MarkAsReadResponse(BaseModel):
    id: str
    isRead: bool
    readAt: datetime

class BulkMarkAsReadRequest(BaseModel):
    notificationIds: List[str]

class BulkMarkAsReadResponse(BaseModel):
    updatedCount: int
    status: str

class DeleteResponse(BaseModel):
    message: str

# Mock data storage
notifications_db = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/me/notifications", response_model=NotificationsResponse)
async def get_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1),
    isRead: Optional[bool] = Query(None),
    type: Optional[str] = Query(None)
):
    """Get paginated notifications for authenticated user."""
    return {
        "page": page,
        "size": size,
        "totalElements": 56,
        "totalPages": 3,
        "notifications": []
    }

@app.get("/users/me/notifications/unread-count", response_model=UnreadCountResponse)
async def get_unread_count():
    """Get unread notification count."""
    return {"unreadCount": 12}

@app.get("/users/me/notifications/{notificationId}", response_model=Notification)
async def get_notification_details(
    notificationId: str = Path(..., description="Notification ID")
):
    """Get complete notification information."""
    return {
        "id": notificationId,
        "type": "ORDER_UPDATE",
        "title": "Order Shipped",
        "message": "Your order #ORD123 has been shipped.",
        "priority": "HIGH",
        "isRead": False,
        "createdAt": datetime.now(),
        "readAt": None,
        "actionUrl": "/orders/ORD123",
        "metadata": {"orderId": "ORD123"}
    }

@app.patch("/users/me/notifications/{notificationId}/read", response_model=MarkAsReadResponse)
async def mark_notification_as_read(
    notificationId: str = Path(..., description="Notification ID"),
    request: MarkAsReadRequest = None
):
    """Mark notification as read."""
    return {
        "id": notificationId,
        "isRead": True,
        "readAt": datetime.now()
    }

@app.patch("/users/me/notifications/read", response_model=BulkMarkAsReadResponse)
async def mark_multiple_notifications_as_read(
    request: BulkMarkAsReadRequest
):
    """Bulk update multiple notifications as read."""
    return {
        "updatedCount": len(request.notificationIds),
        "status": "SUCCESS"
    }

@app.patch("/users/me/notifications/read-all", response_model=BulkMarkAsReadResponse)
async def mark_all_notifications_as_read():
    """Mark all notifications as read."""
    return {
        "updatedCount": 27,
        "status": "SUCCESS"
    }

@app.delete("/users/me/notifications/{notificationId}", response_model=DeleteResponse)
async def delete_notification(
    notificationId: str = Path(..., description="Notification ID")
):
    """Delete a notification."""
    return {"message": "Notification deleted successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)