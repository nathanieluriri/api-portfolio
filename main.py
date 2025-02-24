from Portfolios.imports import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None,redoc_url=None)
origins=[
    "https://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.mount("/v1/product-design",ui_ux_app)
app.mount("/v1/web-design",web_designer_app)
app.mount("/v1/mobile-dev",mobile_dev_app)
app.mount("/v1/machine-learning",machine_learning_app)
app.mount("/v1/backend-dev",backend_app)

@app.get("/")
def home():
    return {"deployed"}