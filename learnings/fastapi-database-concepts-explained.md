# FastAPI Database Concepts Explained in Plain English

## Introduction

If you're learning FastAPI and feeling overwhelmed by all the database-related concepts like SQLAlchemy, SQLModel, sessions, dependencies, and services - you're not alone! This blog post will break down everything in simple terms using your actual code as examples.

## What We're Building

Your project is a shipment tracking API that can:
- Create new shipments
- Get shipment details by ID
- Update shipment information
- Delete shipments

Let's understand how the database pieces fit together!

## 1. Configuration (The Setup)

**File: `app/config.py`**

Think of configuration as the "settings" for your database connection. It's like filling out a form with your database details:

```python
class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str      # Where your database lives
    POSTGRES_PORT: int        # Which door to knock on
    POSTGRES_USERNAME: str    # Your username
    POSTGRES_PASSWORD: str    # Your password
    POSTGRES_DATABASE: str    # Which database to use
```

The `@property` creates a complete database URL that looks like:
`postgresql+asyncpg://username:password@server:port/database`

**Why this matters:** This is like having the address and key to your database house. Without this, your app doesn't know where to find or how to connect to your data.

## 2. Database Models (Your Data Blueprint)

**File: `app/database/models.py`**

Models are like blueprints for your data. They define what information you want to store and how it should look.

```python
class Shipment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Unique identifier
    content: str                                      # What's being shipped
    weight: float = Field(le=25)                     # Weight (max 25)
    destination: int                                 # Where it's going
    status: ShipmentStatus                          # Current status
    estimated_delivery: datetime                     # When it should arrive
```

**What's happening here:**
- `SQLModel` is a modern way to define database tables using Python classes
- `table=True` tells SQLModel "this is a database table"
- `Field(primary_key=True)` means this field uniquely identifies each record
- `Field(le=25)` adds validation (weight must be 25 or less)

**Think of it like:** You're designing a form that everyone must fill out when creating a shipment. Each field has rules about what kind of data it accepts.

## 3. Database Session (Your Connection to the Database)

**File: `app/database/session.py`**

A session is like having an active conversation with your database. It's how you send commands and receive data.

```python
engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True  # This prints SQL commands to console (helpful for debugging)
)

async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False 
    )

    async with async_session() as session:
        yield session
```

**What's happening:**
- `engine` is like the car that drives to your database
- `sessionmaker` creates a factory for making database sessions
- `get_session()` is a function that gives you an active session
- `yield session` means "here's your session, use it, then I'll clean it up"

**Why `yield`?** It's like lending someone a book. You give it to them, they use it, and when they're done, you get it back and put it away properly.

## 4. Dependencies (Getting What You Need)

**File: `app/api/dependencies.py`**

Dependencies are like saying "I need this thing to do my job." FastAPI automatically provides it for you.

```python
SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
```

**What's happening:**
- `SessionDep` is a shortcut that says "I need a database session"
- `get_shipment_service()` takes a session and creates a service object
- `ServiceDep` is a shortcut that says "I need a shipment service"

**Think of it like:** You're a chef in a restaurant. You need ingredients (dependencies) to cook. The kitchen manager (FastAPI) automatically brings you what you need when you ask for it.

## 5. Services (Your Business Logic)

**File: `app/services/shipment.py`**

Services contain the actual business logic - the "how to do things" part of your application.

```python
class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session  # Gets a database session

    async def get(self, id: int) -> Shipment:
        return await self.session.get(Shipment, id)  # Find shipment by ID

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3)
        )

        self.session.add(new_shipment)      # Add to database
        await self.session.commit()         # Save changes
        await self.session.refresh(new_shipment)  # Get updated data

        return new_shipment
```

**What's happening:**
- `get()` finds a shipment by its ID
- `add()` creates a new shipment with default values (status = "placed", delivery in 3 days)
- `session.add()` puts the new shipment in the database
- `session.commit()` saves the changes permanently
- `session.refresh()` gets the updated data (like the auto-generated ID)

**Think of it like:** You're a warehouse manager. You know how to:
- Find packages by their tracking number
- Create new shipments with proper labels
- Update shipment status
- Remove shipments from the system

## 6. Schemas (Data Validation)

**File: `app/api/schemas/shipment.py`**

Schemas define what data looks like when it comes in and goes out of your API.

```python
class ShipmentCreate(BaseShipment):
    pass  # Uses the same fields as BaseShipment

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)  # Optional field
    weight: float | None = Field(default=None, le=25)
    status: ShipmentStatus | None = Field(default=None)
```

**What's happening:**
- `ShipmentCreate` defines what data is needed to create a shipment
- `ShipmentUpdate` defines what data can be updated (all fields are optional)
- `| None` means the field is optional
- `Field(default=None)` gives a default value if nothing is provided

**Think of it like:** You're a bouncer at a club. You check IDs (validate data) before letting people in. Some people need full ID (create), others just need to show they're on the guest list (update).

## 7. API Routes (The Front Door)

**File: `app/api/router.py`**

Routes are like the front desk of your API. They receive requests and send responses.

```python
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    return shipment
```

**What's happening:**
- `@router.get("/shipment")` means "when someone visits /shipment with GET"
- `service: ServiceDep` automatically gets you a shipment service
- `await service.get(id)` finds the shipment
- If not found, return a 404 error
- If found, return the shipment data

**Think of it like:** You're a receptionist. Someone asks "Where's package #123?" You:
1. Look up the package (service.get)
2. If you find it, give it to them
3. If you don't find it, say "Sorry, that package doesn't exist"

## How It All Works Together

Here's the flow when someone wants to get a shipment:

1. **Request comes in:** `GET /shipment?id=123`
2. **FastAPI checks dependencies:** "I need a database session and a service"
3. **Session is created:** Connection to database is established
4. **Service is created:** ShipmentService gets the session
5. **Route calls service:** `service.get(123)`
6. **Service queries database:** `session.get(Shipment, 123)`
7. **Database returns data:** Shipment object with all details
8. **Response is sent back:** JSON with shipment information

## Key Concepts Summary

- **Models** = What your data looks like (like a form template)
- **Sessions** = Active connection to your database (like a phone call)
- **Dependencies** = "I need this to do my job" (like asking for tools)
- **Services** = Business logic (like knowing how to do your job)
- **Schemas** = Data validation (like checking IDs at the door)
- **Routes** = API endpoints (like the front desk)

## Why This Architecture?

This separation of concerns makes your code:
- **Testable:** You can test each piece separately
- **Maintainable:** Changes in one part don't break others
- **Reusable:** Services can be used by different routes
- **Clean:** Each file has a single responsibility

## Common Confusion Points

1. **SQLAlchemy vs SQLModel:** SQLModel is built on top of SQLAlchemy but with a simpler, more modern interface
2. **Async vs Sync:** Your code uses `async/await` because it's more efficient for web applications
3. **Dependencies vs Services:** Dependencies are how you get things, services are what you do with them
4. **Models vs Schemas:** Models define database structure, schemas define API input/output

## Next Steps

Now that you understand the concepts, try:
1. Adding a new field to your Shipment model
2. Creating a new service method
3. Adding a new API endpoint
4. Understanding how the data flows through your application

Remember: The database is just a place to store and retrieve data. All the complexity is in organizing your code so it's easy to understand and maintain! 