from fastapi import APIRouter, Request, status, UploadFile
from typing import Union
from app.security import valid_header
from app.config import API_KEY, SEND_GS
from app.config import worksheet, worksheet_data_users
from app.payments.services import get_row
from app.payments.utils import (
    process_uploaded_file,
    select_bank,
    get_bank_data,
    update_worksheet
)
from app.payments.utils import get_data_user

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/upload_payment_file", status_code=status.HTTP_201_CREATED)
async def upload_payment_file(file: Union[UploadFile, None], request: Request):
    try:
        valid_header(request, API_KEY)
        if not file:
            return {"message": "No file uploaded"}
        row_to_add = get_row(worksheet)
        result_list = process_uploaded_file(file)
        banks = ["INTERBANK", "BBVA", "SCOTIABANK", "BANBIF"]
        selection = select_bank(result_list, banks)
        matches_dict = get_bank_data(selection, result_list)
        matches_dict_additional = {
            "Titular": "",
            "Comision": "",
            "Devolucion": "",
            "Numero cuenta": "",
            "Comunidad": ""
        }
        print(matches_dict)
        print("DNI")
        print(matches_dict.get("DNI", ""))
        # matches_dict["DNI"] = '04641439r'
        user_data = get_data_user(worksheet_data_users, matches_dict.get("DNI", ""))
        bank_number = matches_dict.get('Banco')
        total = matches_dict.get('Total')
        if user_data:
            account_number = user_data[bank_number + 4]
            matches_dict["Titular"] = user_data[1] 
            matches_dict["Comision"] = user_data[4] 
            comision = float(user_data[4].replace(',', '').replace('%', ''))/100
            matches_dict["Devolucion"] = total * (1 - comision) 
            matches_dict["Numero cuenta"] = account_number
            matches_dict["Comunidad"] = user_data[11]

        matches_dict.update(matches_dict_additional)
        to_send = SEND_GS == "True"
        if to_send:
            update_worksheet(worksheet, row_to_add, matches_dict)

        return {'message': 'File uploaded successfully', 'row': row_to_add, 'data': matches_dict}
    except Exception as e:
         return {'message': 'An error occurred', 'error': str(e)}

