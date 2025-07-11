from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.routers.router_interaccion_api_externa import router_ext_api
from app.endpoints.routers.router_db import router_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_ext_api)
app.include_router(router_db)

