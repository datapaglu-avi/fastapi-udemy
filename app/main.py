from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment, ShipmentStatus

from .database.session import SessionDep, create_db_tables
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield
    print('Server stoped')

app = FastAPI(lifespan=lifespan_handler)

### Shipments database
# db = Database()

###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    # shipment = db.get(id)
    shipment = session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    # new_id = db.create(shipment)
    # Return id for later use

    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )

    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # shipment = db.update(id, shipment)

    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No data provided to update'
        )
    
    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    # Remove from datastore
    # db.delete(id)

    session.delete(session.get(Shipment, id))
    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
