# API Contracts & Backend Integration Plan

## Overview
Portfolio website backend for handling contact form submissions and storing messages in MongoDB.

---

## Current Frontend Implementation (MOCKED)

### Mock Data (`/app/frontend/src/data/mock.js`)
- **portfolioData**: Static data for personal info, about, skills, experience, projects, education, certifications, articles
- **All content is currently static** - no database integration

### Mock Functionality (`/app/frontend/src/components/Contact.js`)
- Contact form submission uses `useToast` to show success message
- Form data is **NOT** persisted anywhere
- Form clears after submission (local state only)

---

## Backend API Endpoints to Implement

### 1. POST `/api/contact` - Submit Contact Form
**Purpose**: Store contact form submissions in MongoDB

**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "subject": "string (required)",
  "message": "string (required)"
}
```

**Response Success (201)**:
```json
{
  "success": true,
  "message": "Message sent successfully!",
  "data": {
    "id": "string",
    "name": "string",
    "email": "string",
    "subject": "string",
    "message": "string",
    "timestamp": "datetime",
    "status": "unread"
  }
}
```

**Response Error (400)**:
```json
{
  "success": false,
  "message": "Validation error message",
  "errors": ["field1", "field2"]
}
```

---

### 2. GET `/api/contact` - Retrieve All Messages (Admin)
**Purpose**: Fetch all contact messages for portfolio owner

**Response Success (200)**:
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": "string",
      "name": "string",
      "email": "string",
      "subject": "string",
      "message": "string",
      "timestamp": "datetime",
      "status": "unread|read"
    }
  ]
}
```

---

### 3. GET `/api/contact/:id` - Get Single Message (Optional)
**Purpose**: Retrieve specific contact message

**Response Success (200)**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "name": "string",
    "email": "string",
    "subject": "string",
    "message": "string",
    "timestamp": "datetime",
    "status": "unread|read"
  }
}
```

---

## MongoDB Schema

### Collection: `contact_messages`

```python
{
  "_id": ObjectId,
  "id": "string (UUID)",
  "name": "string",
  "email": "string",
  "subject": "string",
  "message": "string",
  "timestamp": "datetime (UTC)",
  "status": "string (unread|read)",
  "ip_address": "string (optional)",
  "user_agent": "string (optional)"
}
```

**Indexes**:
- `id`: unique
- `email`: non-unique
- `timestamp`: descending (for sorting)
- `status`: non-unique (for filtering)

---

## Frontend Integration Changes

### File: `/app/frontend/src/components/Contact.js`

**Current (Mock)**:
```javascript
const handleSubmit = (e) => {
  e.preventDefault();
  // Mock submission
  toast({
    title: 'Message Sent!',
    description: "Thank you for reaching out. I'll get back to you soon!",
    duration: 5000
  });
  setFormData({ name: '', email: '', subject: '', message: '' });
};
```

**After Integration**:
```javascript
const [isSubmitting, setIsSubmitting] = useState(false);

const handleSubmit = async (e) => {
  e.preventDefault();
  setIsSubmitting(true);
  
  try {
    const response = await axios.post(`${API}/contact`, formData);
    
    toast({
      title: 'Message Sent!',
      description: response.data.message || "Thank you for reaching out!",
      duration: 5000
    });
    
    setFormData({ name: '', email: '', subject: '', message: '' });
  } catch (error) {
    toast({
      title: 'Error',
      description: error.response?.data?.message || 'Failed to send message. Please try again.',
      variant: 'destructive',
      duration: 5000
    });
  } finally {
    setIsSubmitting(false);
  }
};
```

**UI Changes**:
- Add loading state to submit button
- Disable form during submission
- Show error messages if submission fails

---

## Backend File Structure

```
/app/backend/
├── server.py (main FastAPI app)
├── models/
│   └── contact.py (Pydantic models)
├── routes/
│   └── contact.py (contact endpoints)
├── .env (environment variables)
└── requirements.txt (dependencies)
```

---

## Implementation Steps

1. ✅ **Create MongoDB Model** - Define ContactMessage schema
2. ✅ **Create API Routes** - Implement POST, GET endpoints
3. ✅ **Add Validation** - Email format, required fields, string lengths
4. ✅ **Update Frontend** - Replace mock with real API calls
5. ✅ **Add Error Handling** - Frontend error states and messages
6. ✅ **Test Integration** - End-to-end testing with backend testing agent

---

## Notes

- No authentication required for POST (public contact form)
- GET endpoints could be protected later for admin access
- Email notifications can be added later (optional)
- Rate limiting should be considered for production
- CORS is already configured in server.py
