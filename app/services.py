import gspread
import easyocr as ocr

def get_worksheet(credentials, book_name, sheet_name):
    gc = gspread.service_account_from_dict(credentials)
    book = gc.open(book_name)
    worksheet = book.worksheet(sheet_name)
    return worksheet

def get_ocr_model():
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader