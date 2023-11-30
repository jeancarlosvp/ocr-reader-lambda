from app.config import reader
from app.payments.services import (
    get_data_bcp,
    get_data_ibk,
    get_data_scotiabank,
    get_data_banbif,
    get_data_bbva
)
from datetime import datetime

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
    
def update_worksheet(worksheet, row_to_add, matches_dict):
    try:
        date_now = datetime.now().strftime("%d/%m/%Y")
        worksheet.batch_update([
            {
                'range': f'B{row_to_add}:C{row_to_add}',
                'values': [[date_now, matches_dict.get("DNI", "")]]
            },
            {
                'range': f'F{row_to_add}:G{row_to_add}',
                'values': [[matches_dict.get("Total", ""), matches_dict.get("Banco", "")]]
            },
            {
                'range': f'P{row_to_add}:R{row_to_add}',
                'values': [["DS", matches_dict.get("Codigo de operacion", "-"), matches_dict.get("Numero tarjeta", "")]]
            }
        ], value_input_option='USER_ENTERED')

    except Exception as e:
        print(e)
        return {"message": "Error updating worksheet"}
    
def get_data_user(worksheet_data_user, dni):
    try:
        values_list = worksheet_data_user.get_all_values()
        values_list = values_list[4:]
        dni_index = 0
        user_data = next((row for row in values_list if row[dni_index] == dni), None)
        return user_data
    except Exception as e:
        print(e)
        return {"message": "Error getting user data"}