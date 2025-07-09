from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


# Could not name the endpoint as docs, since it clashed with the API doc site
@app.get('/shipment')
def get_shipment():
    print(app.openapi_url)

    return {
        "content": "Bomber Jacket",
        "status": "Delivered"
    }


@app.get('/scalar', include_in_schema = False)
def get_scalar_docs():
    return get_scalar_api_reference (
        openapi_url = app.openapi_url,
        title = 'Scalar API'
    )