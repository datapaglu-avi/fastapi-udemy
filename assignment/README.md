# FastAPI Assignment - Shipment Management System

## Overview
This assignment is designed to test your understanding of the FastAPI concepts you've learned so far. You'll be working with the existing shipment management system and extending it with new features.

## Topics Covered in This Assignment
- FastAPI basics and routing
- Pydantic models and data validation
- SQLModel for database operations
- CRUD operations (Create, Read, Update, Delete)
- HTTP status codes and error handling
- Dependency injection
- Database session management
- Enum usage for status management
- API documentation with Scalar

---

## Assignment 1: Customer Management System

### Task Description
Extend your shipment system to include customer management functionality.

### Requirements

#### 1.1 Create Customer Models
Create a new file `app/database/customer_models.py` with the following:

```python
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel

class CustomerType(str, Enum):
    individual = "individual"
    business = "business"
    premium = "premium"

class Customer(SQLModel, table=True):
    __tablename__ = 'customer'
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    phone: str = Field(min_length=10, max_length=15)
    customer_type: CustomerType = Field(default=CustomerType.individual)
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
```

#### 1.2 Create Customer Schemas
Create a new file `app/schemas/customer_schemas.py` with:

```python
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from app.database.customer_models import CustomerType

class CustomerBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    phone: str = Field(min_length=10, max_length=15)
    customer_type: CustomerType = Field(default=CustomerType.individual)

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime
    is_active: bool

class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: str | None = Field(default=None, regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    phone: str | None = Field(default=None, min_length=10, max_length=15)
    customer_type: CustomerType | None = Field(default=None)
    is_active: bool | None = Field(default=None)
```

#### 1.3 Implement Customer CRUD Operations
Add the following endpoints to your `main.py`:

```python
# Customer endpoints
@app.post("/customers", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, session: SessionDep):
    # Implementation here
    pass

@app.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, session: SessionDep):
    # Implementation here
    pass

@app.get("/customers", response_model=list[CustomerRead])
def list_customers(skip: int = 0, limit: int = 10, session: SessionDep):
    # Implementation here
    pass

@app.patch("/customers/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer_update: CustomerUpdate, session: SessionDep):
    # Implementation here
    pass

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, session: SessionDep):
    # Implementation here
    pass
```

### Deliverables
- Complete implementation of all customer CRUD operations
- Proper error handling for all endpoints
- Validation of input data
- Database integration with SQLModel

---

## Assignment 2: Enhanced Shipment Features

### Task Description
Enhance the existing shipment system with additional features and validations.

### Requirements

#### 2.1 Add Shipment Priority
Modify the `ShipmentStatus` enum to include priority levels:

```python
class ShipmentPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"
```

Update the `Shipment` model to include:
- `priority: ShipmentPriority = Field(default=ShipmentPriority.normal)`
- `customer_id: int = Field(foreign_key="customer.id")`

#### 2.2 Implement Shipment Search and Filtering
Add these endpoints to your `main.py`:

```python
@app.get("/shipments/search")
def search_shipments(
    status: ShipmentStatus | None = None,
    priority: ShipmentPriority | None = None,
    customer_id: int | None = None,
    min_weight: float | None = None,
    max_weight: float | None = None,
    session: SessionDep
):
    # Implementation here
    pass

@app.get("/shipments/statistics")
def get_shipment_statistics(session: SessionDep):
    # Return statistics like:
    # - Total shipments
    # - Shipments by status
    # - Average weight
    # - Shipments by priority
    pass
```

#### 2.3 Add Bulk Operations
Implement bulk shipment operations:

```python
@app.post("/shipments/bulk", response_model=list[ShipmentRead])
def create_bulk_shipments(shipments: list[ShipmentCreate], session: SessionDep):
    # Implementation here
    pass

@app.patch("/shipments/bulk/status")
def update_bulk_shipment_status(
    shipment_ids: list[int], 
    new_status: ShipmentStatus, 
    session: SessionDep
):
    # Implementation here
    pass
```

### Deliverables
- Updated shipment model with priority and customer relationship
- Search and filtering functionality
- Statistics endpoint
- Bulk operations implementation
- Proper error handling and validation

---

## Assignment 3: Advanced Features

### Task Description
Implement advanced features to demonstrate deeper FastAPI knowledge.

### Requirements

#### 3.1 Add Authentication (Basic)
Create a simple authentication system:

```python
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Implement basic authentication
    # Return user info or raise HTTPException
    pass
```

#### 3.2 Add Rate Limiting
Implement rate limiting for your endpoints:

```python
from fastapi import Request
import time
from collections import defaultdict

# Simple in-memory rate limiter
request_counts = defaultdict(list)

def rate_limit(request: Request, max_requests: int = 10, window_seconds: int = 60):
    # Implementation here
    pass
```

#### 3.3 Add Caching
Implement caching for frequently accessed data:

```python
from functools import lru_cache
import time

# Simple cache implementation
cache = {}

def get_cached_data(key: str, ttl_seconds: int = 300):
    # Implementation here
    pass
```

#### 3.4 Add Logging
Implement comprehensive logging:

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add logging to your endpoints
```

### Deliverables
- Basic authentication system
- Rate limiting implementation
- Caching mechanism
- Comprehensive logging
- Protected endpoints using authentication

---

## Assignment 4: Testing

### Task Description
Create comprehensive tests for your API endpoints.

### Requirements

#### 4.1 Unit Tests
Create `tests/test_main.py` with:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_shipment():
    # Test shipment creation
    pass

def test_get_shipment():
    # Test shipment retrieval
    pass

def test_update_shipment():
    # Test shipment update
    pass

def test_delete_shipment():
    # Test shipment deletion
    pass

def test_create_customer():
    # Test customer creation
    pass

# Add more test cases
```

#### 4.2 Integration Tests
Create integration tests that test the full flow:

```python
def test_shipment_workflow():
    # Test complete shipment workflow
    # 1. Create customer
    # 2. Create shipment for customer
    # 3. Update shipment status
    # 4. Verify final state
    pass
```

### Deliverables
- Comprehensive unit tests
- Integration tests
- Test coverage for error cases
- Test data fixtures

---

## Assignment 5: Documentation and API Design

### Task Description
Improve API documentation and design.

### Requirements

#### 5.1 Enhanced API Documentation
- Add detailed docstrings to all endpoints
- Include example requests and responses
- Add proper response models
- Include error response documentation

#### 5.2 API Versioning
Implement API versioning:

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

# Add your endpoints to appropriate routers
```

#### 5.3 OpenAPI Customization
Customize your OpenAPI documentation:

```python
app = FastAPI(
    title="Shipment Management API",
    description="A comprehensive API for managing shipments and customers",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
```

### Deliverables
- Enhanced API documentation
- API versioning implementation
- Customized OpenAPI schema
- Example requests and responses

---

## Submission Guidelines

### What to Submit
1. **Complete source code** for all assignments
2. **README.md** with setup and usage instructions
3. **Requirements.txt** or **pyproject.toml** with all dependencies
4. **Test results** showing all tests passing
5. **API documentation** (can be generated from your FastAPI app)

### Code Quality Requirements
- Follow PEP 8 style guidelines
- Include proper error handling
- Add comprehensive docstrings
- Use type hints throughout
- Implement proper validation
- Handle edge cases

### Testing Requirements
- All endpoints should have corresponding tests
- Test both success and error scenarios
- Achieve at least 80% code coverage
- Include integration tests

### Bonus Points
- Implement async database operations
- Add background tasks
- Implement WebSocket endpoints
- Add database migrations
- Implement pagination for list endpoints
- Add request/response middleware
- Implement custom exception handlers

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

1. **Fork/Clone** this repository
2. **Create a new branch** for your assignment work
3. **Implement** each assignment step by step
4. **Test** your implementation thoroughly
5. **Document** your code and API
6. **Submit** your completed work

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python Testing with pytest](https://docs.pytest.org/)

Good luck with your assignment! 🚀 