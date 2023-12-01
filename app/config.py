from starlette.config import Config
from app.services import get_ocr_model

config = Config("./.env")

CORS_ORIGIN = config("CORS_ORIGIN")
API_KEY = config("API_KEY")

SEND_GS = config("SEND_GS")
URL_SENDER_GS = config("URL_SENDER_GS")

reader = get_ocr_model()
