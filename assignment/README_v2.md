# FastAPI Assignment - ToDo App Project

## Overview
This assignment will help you apply the FastAPI concepts you've learned by building a complete ToDo application from scratch. You will design, implement, test, and document a RESTful API for managing tasks, users, and advanced features.

## Topics Covered
- FastAPI basics and routing
- Pydantic models and data validation
- SQLModel for database operations
- CRUD operations (Create, Read, Update, Delete)
- HTTP status codes and error handling
- Dependency injection
- Database session management
- Enum usage for status/priority
- API documentation
- Authentication and authorization
- Testing (unit and integration)

---

## Assignment 1: Task Management System

### Task Description
Build a ToDo app backend with FastAPI that allows users to manage their tasks.

### Requirements

#### 1.1 Create Task Models
Create a file `app/database/models.py` with:

```python
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(SQLModel, table=True):
    __tablename__ = 'task'
    id: int = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")
```

#### 1.2 Create User Models
Add a `User` model for authentication:

```python
class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=3, max_length=50)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
```

#### 1.3 Create Schemas
Create `app/schemas.py` with Pydantic models for Task and User (Create, Read, Update).

#### 1.4 Implement CRUD Endpoints
In `main.py`, implement endpoints for:
- Creating, reading, updating, deleting tasks
- Listing tasks (with filtering by status, priority, due date, etc.)
- Creating and managing users

---

## Assignment 2: Advanced Features

### Task Description
Add advanced features to your ToDo app.

### Requirements

#### 2.1 Task Search and Filtering
- Implement endpoints to search/filter tasks by status, priority, due date, and user.

#### 2.2 Task Statistics
- Add an endpoint to return statistics (e.g., total tasks, completed tasks, overdue tasks, tasks by priority).

#### 2.3 Bulk Operations
- Implement bulk creation and status update for tasks.

#### 2.4 Soft Delete and Archiving
- Implement soft delete (archiving) for tasks instead of hard delete.

---

## Assignment 3: Authentication & Authorization

### Task Description
Secure your API with authentication and user-based access control.

### Requirements

#### 3.1 User Registration & Login
- Implement user registration and login endpoints.
- Use password hashing (e.g., passlib).

#### 3.2 JWT Authentication
- Secure all task endpoints so only authenticated users can access their own tasks.
- Use JWT tokens for authentication.

#### 3.3 Role-based Access (Bonus)
- Add an `is_admin` field to the User model.
- Allow admin users to manage all tasks and users.

---

## Assignment 4: Testing

### Task Description
Write tests for your API.

### Requirements

#### 4.1 Unit Tests
- Test task and user CRUD operations.
- Test authentication logic.

#### 4.2 Integration Tests
- Test full user-task workflows (register, login, create task, update, delete, etc.).

#### 4.3 Error Cases
- Test error handling (invalid data, unauthorized access, etc.).

---

## Assignment 5: Documentation & API Design

### Task Description
Document your API and improve its design.

### Requirements

#### 5.1 Enhanced API Documentation
- Add docstrings to all endpoints.
- Provide example requests and responses.
- Document error responses.

#### 5.2 OpenAPI Customization
- Customize your FastAPI app’s OpenAPI schema (title, description, version, contact, etc.).

#### 5.3 API Versioning (Bonus)
- Implement API versioning using FastAPI routers.

---

## Submission Guidelines

### What to Submit
1. **Complete source code** for the ToDo app
2. **README.md** with setup and usage instructions
3. **Requirements.txt** or **pyproject.toml** with all dependencies
4. **Test results** showing all tests passing
5. **API documentation** (generated from your FastAPI app)

### Code Quality Requirements
- Follow PEP 8 style guidelines
- Proper error handling
- Comprehensive docstrings
- Use type hints
- Input validation
- Handle edge cases

### Testing Requirements
- All endpoints should have tests
- Test both success and error scenarios
- At least 80% code coverage
- Include integration tests

### Bonus Points
- Async database operations
- Background tasks (e.g., reminders)
- WebSocket endpoints (e.g., real-time updates)
- Database migrations
- Pagination for list endpoints
- Middleware (e.g., logging, request/response)
- Custom exception handlers

---

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Functionality | 40% |
| Code Quality | 25% |
| Testing | 20% |
| Documentation | 10% |
| Bonus Features | 5% |

---

## Getting Started

1. **Create a new FastAPI project** (do not extend the shipment app)
2. **Set up a virtual environment** and install dependencies
3. **Implement** each assignment step by step
4. **Test** your implementation thoroughly
5. **Document** your code and API
6. **Submit** your completed work

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [Passlib (Password Hashing)](https://passlib.readthedocs.io/)
- [PyJWT (JWT Tokens)](https://pyjwt.readthedocs.io/)

Good luck building your ToDo app! 🚀 