from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGIN
from typing import Dict
from app.payments.routers import router as payments_router

app = FastAPI()

print("okokokok")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments_router)

@app.get("/")
def root() -> Dict[str, object]:
    return {"message": "Bienvenido al servicio ocr-worksheet"}

