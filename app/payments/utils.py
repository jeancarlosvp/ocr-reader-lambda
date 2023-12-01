from app.config import reader
from app.payments.services import (
    get_data_bcp,
    get_data_ibk,
    get_data_scotiabank,
    get_data_banbif,
    get_data_bbva
)

BANK_FUNCTIONS = {
    "BCP": get_data_bcp,
    "INTERBANK": get_data_ibk,
    "BBVA": get_data_bbva,
    "SCOTIABANK": get_data_scotiabank,
    "BANBIF": get_data_banbif,
}

def process_uploaded_file(file):
    try:
        result = reader.readtext(file.file.read(), paragraph=True)
        return [item[1].upper() for item in result]
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return []

def select_bank(result_list, banks):
    try:
        return next((bank for bank in banks if bank in result_list), "BCP")
    except StopIteration:
        return "BCP"
    
def get_bank_data(selection, result_list):
    try:
        if selection in BANK_FUNCTIONS:
            return BANK_FUNCTIONS[selection](result_list)
        else:
            return {"message": "No bank found"}
    except Exception as e:
        print(f"Error getting bank data: {str(e)}")
        return {}
    
    
