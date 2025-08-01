from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.api.router import router
from .database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield
    print('Server stoped')

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
