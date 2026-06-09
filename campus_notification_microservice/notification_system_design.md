#Stage1

# Notification Platform REST API Design

## 1. Overview

This document defines the REST API contract for a notification platform that displays notifications to authenticated users when they are logged in.

### Objectives

* Retrieve user notifications
* Retrieve unread notification count
* Mark notifications as read
* Mark all notifications as read
* Delete notifications
* Support real-time notification delivery
* Maintain consistent API design conventions

### Base URL



### Common Headers

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: application/json
```

---

# 2. Notification Resource Model

## Notification Object

```json
{
  "id": "ntf_123456",
  "type": "ORDER_UPDATE",
  "title": "Order Shipped",
  "message": "Your order #ORD123 has been shipped.",
  "priority": "HIGH",
  "isRead": false,
  "createdAt": "2026-06-09T10:15:30Z",
  "readAt": null,
  "actionUrl": "/orders/ORD123",
  "metadata": {
    "orderId": "ORD123"
  }
}
```

## Field Definitions

| Field     | Type     | Description                    |
| --------- | -------- | ------------------------------ |
| id        | String   | Unique notification identifier |
| type      | String   | Notification category          |
| title     | String   | Notification title             |
| message   | String   | Notification message           |
| priority  | String   | LOW, MEDIUM, HIGH              |
| isRead    | Boolean  | Read status                    |
| createdAt | DateTime | Creation timestamp             |
| readAt    | DateTime | Read timestamp                 |
| actionUrl | String   | UI navigation target           |
| metadata  | Object   | Additional context             |

---

# 3. Core Actions Supported

1. Get Notifications
2. Get Unread Count
3. Get Notification Details
4. Mark Notification as Read
5. Mark Multiple Notifications as Read
6. Mark All Notifications as Read
7. Delete Notification
8. Real-Time Notification Delivery

---

# 4. API Endpoints

## 4.1 Get Notifications

Returns paginated notifications for the authenticated user.

### Endpoint

```http
GET /users/me/notifications
```

### Query Parameters

| Parameter | Type    | Required | Description                 |
| --------- | ------- | -------- | --------------------------- |
| page      | Integer | No       | Page number                 |
| size      | Integer | No       | Page size                   |
| isRead    | Boolean | No       | Filter by read status       |
| type      | String  | No       | Filter by notification type |

### Request

```http
GET /users/me/notifications?page=1&size=20&isRead=false
Authorization: Bearer <token>
```

### Response

```json
{
  "page": 1,
  "size": 20,
  "totalElements": 56,
  "totalPages": 3,
  "notifications": [
    {
      "id": "ntf_123456",
      "type": "ORDER_UPDATE",
      "title": "Order Shipped",
      "message": "Your order has been shipped.",
      "priority": "HIGH",
      "isRead": false,
      "createdAt": "2026-06-09T10:15:30Z",
      "actionUrl": "/orders/ORD123"
    }
  ]
}
```

### Status Codes

```http
200 OK
401 Unauthorized
500 Internal Server Error
```

---

## 4.2 Get Unread Notification Count

Returns unread notification count.

### Endpoint

```http
GET /users/me/notifications/unread-count
```

### Response

```json
{
  "unreadCount": 12
}
```

### Status Codes

```http
200 OK
401 Unauthorized
```

---

## 4.3 Get Notification Details

Returns complete notification information.

### Endpoint

```http
GET /users/me/notifications/{notificationId}
```

### Example

```http
GET /users/me/notifications/ntf_123456
```

### Response

```json
{
  "id": "ntf_123456",
  "type": "ORDER_UPDATE",
  "title": "Order Shipped",
  "message": "Your order #ORD123 has been shipped.",
  "priority": "HIGH",
  "isRead": false,
  "createdAt": "2026-06-09T10:15:30Z",
  "readAt": null,
  "actionUrl": "/orders/ORD123",
  "metadata": {
    "orderId": "ORD123"
  }
}
```

---

## 4.4 Mark Notification as Read

Updates notification read status.

### Endpoint

```http
PATCH /users/me/notifications/{notificationId}/read
```

### Request

```json
{
  "isRead": true
}
```

### Response

```json
{
  "id": "ntf_123456",
  "isRead": true,
  "readAt": "2026-06-09T10:30:45Z"
}
```

### Status Codes

```http
200 OK
404 Not Found
```

---

## 4.5 Mark Multiple Notifications as Read

Bulk update notifications.

### Endpoint

```http
PATCH /users/me/notifications/read
```

### Request

```json
{
  "notificationIds": [
    "ntf_123",
    "ntf_124",
    "ntf_125"
  ]
}
```

### Response

```json
{
  "updatedCount": 3,
  "status": "SUCCESS"
}
```

---

## 4.6 Mark All Notifications as Read

Marks every notification for the current user as read.

### Endpoint

```http
PATCH /users/me/notifications/read-all
```

### Request

```json
{}
```

### Response

```json
{
  "updatedCount": 27,
  "status": "SUCCESS"
}
```

---

## 4.7 Delete Notification

Deletes a notification.

### Endpoint

```http
DELETE /users/me/notifications/{notificationId}
```

### Request

```http
DELETE /users/me/notifications/ntf_123456
```

### Response

```json
{
  "message": "Notification deleted successfully."
}
```

### Status Codes

```http
204 No Content
404 Not Found
```

---

# 5. Standard Error Response

All APIs should return a consistent error format.

```json
{
  "timestamp": "2026-06-09T10:30:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Invalid notification ID",
  "path": "/users/me/notifications/abc"
}
```

---

# 6. Real-Time Notification Mechanism

## Recommended Approach: WebSocket

REST APIs are suitable for retrieval and updates, but real-time notifications should use WebSockets.

### Connection Endpoint

```http
wss://api.example.com/v1/notifications/ws
```

### Connection Headers

```http
Authorization: Bearer <JWT_TOKEN>
```

---

## Real-Time Event Structure

### New Notification Event

```json
{
  "eventType": "NEW_NOTIFICATION",
  "timestamp": "2026-06-09T10:45:00Z",
  "data": {
    "id": "ntf_987654",
    "type": "PAYMENT_SUCCESS",
    "title": "Payment Received",
    "message": "Your payment has been processed.",
    "priority": "MEDIUM",
    "isRead": false,
    "createdAt": "2026-06-09T10:45:00Z",
    "actionUrl": "/payments/PAY123"
  }
}
```

### Notification Updated Event

```json
{
  "eventType": "NOTIFICATION_UPDATED",
  "timestamp": "2026-06-09T10:46:00Z",
  "data": {
    "notificationId": "ntf_987654",
    "isRead": true
  }
}
```

### Notification Deleted Event

```json
{
  "eventType": "NOTIFICATION_DELETED",
  "timestamp": "2026-06-09T10:47:00Z",
  "data": {
    "notificationId": "ntf_987654"
  }
}
```

---

# 7. Client Flow

## Initial Login

1. User logs in.
2. Client calls:

```http
GET /users/me/notifications
```

3. Client calls:

```http
GET /users/me/notifications/unread-count
```

4. Client establishes WebSocket connection.

```http
wss://api.example.com/v1/notifications/ws
```

5. New notifications arrive instantly through WebSocket events.

---

# 8. Design Principles Used

* Resource-oriented URLs
* Predictable endpoint naming
* Stateless REST operations
* Pagination support
* Consistent error model
* JWT-based authentication
* Bulk operations for scalability
* WebSocket support for real-time delivery
* Backward-compatible response structures

---

# API Summary

| Action                   | Method    | Endpoint                             |
| ------------------------ | --------- | ------------------------------------ |
| Get Notifications        | GET       | /users/me/notifications              |
| Get Notification Details | GET       | /users/me/notifications/{id}         |
| Get Unread Count         | GET       | /users/me/notifications/unread-count |
| Mark Notification Read   | PATCH     | /users/me/notifications/{id}/read    |
| Mark Multiple Read       | PATCH     | /users/me/notifications/read         |
| Mark All Read            | PATCH     | /users/me/notifications/read-all     |
| Delete Notification      | DELETE    | /users/me/notifications/{id}         |
| Real-Time Updates        | WebSocket | /notifications/ws                    |

```
```




Notification Metadata-> SQS (AWS)/NOTIFICATION SERVICE ->USER PHONE



#STAGE 2 
I will use SQL based persistent schema because the notification system is entirely based on user details and using SQL schema we can extract strctured details easily and very fast as compare to NoSQL. We will also get validation of the fetched user details as well.

As the data volume increases, problem that will arise are the following:
  1)Increase in storage size of DB
  2)Heavy load on DB Throughput
  3)Latency in Read/Writes

We can solve this problem by the use of caching using Redis.

What we will do is basically when a fetch request is processed, we will check the cache db of redis and if the details are in there then the user details will be directly sent from cache DB to Client App. 

If the cache DB does not contains the User details we will fetch it from DB using Read operation and store inside the Cache DB with a TTL based expiry.This will ensure that multiple duplicate requests do not directly hit the DB.

We can also implement a messaging queue service like RabbitMQ/Kafka that will take Request and process it slowing in the background ensuring our DB does not get overloaded with requests.


#Stage 3

This query is not accurate.It is slow because it checks each record iteratively and is very slow operation.Adding indexes can help in increasing speed of Read operations however it will not make a big difference if the DB is very huge.

#Stage 4

The DB is getting hit with every request and thus getting overwhelmed.I will suggest two solutions for the problem.

1)Caching - We can use caching DB like Redis to cache responses from the DB
2)Queue Service(Kafka)- It will process requests such that the DB can process it easily and does not get bombarded.
3)Master - Slave DBs : We can use the Master-Slave architecture to make a single DB for write operations called "Master DB" and the read requests will be processed through "Slave DBs". We can use async consistency and the DB will get constient eventually. Sync them.

This will distribute the load to multiple DB and thus reducing load on a single DB.


Tradeoffs: 
  1) There is complexity involved in setting up this infrastructure.
  2) Expensive infrastructure 
  3) There may be increase in latency of getting API responses.

#Stage 5

The problem is we have not used try and except with this code so that when the first function fails all the other functions fail cascadely manner and thus results in whole failure. We can implement Error handling techniques to ensure that if a functions fails to get response we can close the operation gracefully.

We will use a Worker-Producer-Consumer Architecture using Messaging Queue Services.

1) Producer - This will generate the notification metadata
2) Worker-This will transfer and process the notification service
3) Consumer - After the notifications are processed they are sent to mobile devices using SSE (Server Side Events) to their phones directly.

The process of sending the email and saving to DB should not be processed simultaneously.

function notifyall(students_ids:array,message:string):
    for student_id in student_ids:
        try:
          send_email(student_id,message)
          save_to_db(student_id,message)
          push_to_app(student_id,message)
        except:
          return "Process Failed"


#Stage 6


As the new notifications will keep coming we will use an doubly ended queue based data strcture which will store top 10 response and whatever new response comes we will add it to end and remove the first response immediately. This will be like a using a queue which uses FIFO architecture.

