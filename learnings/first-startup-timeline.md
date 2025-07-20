# First App Startup Timeline Flow

## App Initialization (Before First Request)

### 1. **FastAPI App Creation**
```python
# main.py
app = FastAPI(lifespan=lifespan_handler)
```
- FastAPI instance created
- Lifespan handler registered

### 2. **Database Engine Creation**
```python
# database/session.py
engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)
```
- PostgreSQL connection engine created
- Connection pool initialized

### 3. **Database Tables Creation**
```python
# main.py → lifespan_handler
async def lifespan_handler(app: FastAPI):
    await create_db_tables()  # Creates shipment table
    yield
```
- `shipment` table created in PostgreSQL
- Table structure based on `Shipment` model

### 4. **Router Registration**
```python
# main.py
app.include_router(router)
```
- API routes registered with FastAPI

---

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    APP STARTUP PHASE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. FastAPI App Created                                        │
│     ┌─────────────┐                                            │
│     │   FastAPI   │ ← lifespan_handler registered              │
│     │   Instance  │                                            │
│     └─────────────┘                                            │
│              │                                                  │
│              ▼                                                  │
│  2. Database Engine Created                                    │
│     ┌─────────────┐    ┌─────────────┐                        │
│     │ PostgreSQL  │◄───│   Engine    │ ← Connection pool       │
│     │   Database  │    │             │                         │
│     └─────────────┘    └─────────────┘                         │
│              │                                                  │
│              ▼                                                  │
│  3. Tables Created                                             │
│     ┌─────────────┐                                            │
│     │  shipment   │ ← Table created from Shipment model       │
│     │   table     │                                            │
│     └─────────────┘                                            │
│              │                                                  │
│              ▼                                                  │
│  4. Routes Registered                                          │
│     ┌─────────────┐                                            │
│     │    Router   │ ← API endpoints registered                 │
│     │             │                                            │
│     └─────────────┘                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FIRST REQUEST PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  5. Request Received                                           │
│     ┌─────────────┐                                            │
│     │    Client   │ → GET /shipment?id=123                     │
│     └─────────────┘                                            │
│              │                                                  │
│              ▼                                                  │
│  6. Dependency Resolution                                      │
│     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│     │   Service   │◄───│   Session   │◄───│   Engine    │      │
│     │ Dependency  │    │ Dependency  │    │             │      │
│     └─────────────┘    └─────────────┘    └─────────────┘      │
│              │                                                  │
│              ▼                                                  │
│  7. Route Function                                             │
│     ┌─────────────┐                                            │
│     │   Router    │ → get_shipment(id, service)                │
│     │             │                                            │
│     └─────────────┘                                            │
│              │                                                  │
│              ▼                                                  │
│  8. Service Layer                                              │
│     ┌─────────────┐                                            │
│     │   Service   │ → service.get(id)                          │
│     │             │                                            │
│     └─────────────┘                                            │
│              │                                                  │
│              ▼                                                  │
│  9. Database Query                                             │
│     ┌─────────────┐    ┌─────────────┐                        │
│     │   Service   │───►│ PostgreSQL  │ → SELECT * FROM shipment│
│     │             │    │             │                         │
│     └─────────────┘    └─────────────┘                         │
│              │                                                  │
│              ▼                                                  │
│  10. Response Flow                                             │
│     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│     │ PostgreSQL  │───►│   Service   │───►│   Router    │      │
│     │   Result    │    │   Object    │    │   JSON      │      │
│     └─────────────┘    └─────────────┘    └─────────────┘      │
│              │                                                  │
│              ▼                                                  │
│     ┌─────────────┐                                            │
│     │    Client   │ ← JSON Response                            │
│     └─────────────┘                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## First GET Request: `GET /shipment?id=123`

### 5. **Request Reception**
```
Client → FastAPI → Router Matching
```
- FastAPI receives HTTP request
- Matches to `@router.get("/shipment")`

### 6. **Dependency Resolution Chain**
```python
# FastAPI resolves dependencies in order:
ServiceDep → get_shipment_service() → SessionDep → get_session()
```

**Step 6a: Session Creation**
```python
# database/session.py
async def get_session():
    async_session = sessionmaker(bind=engine, class_=AsyncSession)
    async with async_session() as session:
        yield session  # Database connection established
```

**Step 6b: Service Creation**
```python
# api/dependencies.py
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)  # Service with database session
```

### 7. **Route Function Execution**
```python
# api/router.py
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)  # Calls ShipmentService.get(123)
```

### 8. **Service Layer Execution**
```python
# services/shipment.py
async def get(self, id: int) -> Shipment:
    return await self.session.get(Shipment, id)  # Database query
```

### 9. **Database Query**
```sql
-- Generated SQL by SQLAlchemy
SELECT * FROM shipment WHERE id = 123;
```

### 10. **Response Flow**
```
Database Result → Shipment Object → JSON Response → Client
```

---

## Timeline Summary

```
App Startup:
1. FastAPI App Created
2. Database Engine Created  
3. Tables Created (shipment)
4. Routes Registered

First Request:
5. Request Received
6. Dependencies Resolved (Session → Service)
7. Route Function Called
8. Service Method Executed
9. Database Query Run
10. Response Sent
```

## Key Points

- **First startup** creates database tables
- **Each request** creates new session and service instances
- **Dependencies** are resolved automatically by FastAPI
- **Database connection** is managed by SQLAlchemy engine
- **Response** flows back through the same chain in reverse 