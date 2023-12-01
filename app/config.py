from starlette.config import Config
from app.services import get_ocr_model

config = Config("./.env")

CORS_ORIGIN = config("CORS_ORIGIN")
API_KEY = config("API_KEY")

# CREDENTIALS_DICT = {
#     "type": config("TYPE"),
#     "project_id": config("PROJECT_ID"),
#     "private_key_id": config("PRIVATE_KEY_ID"),
#     "private_key": config("PRIVATE_KEY").replace("\\n", "\n"),
#     "client_email": config("CLIENT_EMAIL"),
#     "client_id": config("CLIENT_ID"),
#     "auth_uri": config("AUTH_URI"),
#     "token_uri": config("TOKEN_URI"),
#     "auth_provider_x509_cert_url": config("AUTH_PROVIDER_X509_CERT_URL"),
#     "client_x509_cert_url": config("CLIENT_X509_CERT_URL"),
#     "universe_domain": config("UNIVERSE_DOMAIN")
# }

# BOOK_ID = config("BOOK_ID")
# SHEET_PAYMENT = config("SHEET_PAYMENT")

SEND_GS = config("SEND_GS")

# worksheet = get_worksheet(CREDENTIALS_DICT, BOOK_ID, SHEET_PAYMENT)
reader = get_ocr_model()
