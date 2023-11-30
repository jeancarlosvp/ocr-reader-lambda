from fastapi import APIRouter, Request, status, UploadFile
from typing import Union
from app.security import valid_header
from app.config import API_KEY, SEND_GS
from app.config import worksheet
from app.payments.services import get_row
from app.payments.utils import (
    process_uploaded_file,
    select_bank,
    get_bank_data,
    update_worksheet
)

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
        print(matches_dict)
        to_send = SEND_GS == "True"
        if to_send:
            update_worksheet(worksheet, row_to_add, matches_dict)

        return {'mensaje': 'Imagen subida satisfactoriamente', 'se agregó en la fila': row_to_add, 'datos': matches_dict}
    except Exception as e:
         return {'message': 'An error occurred', 'error': str(e)}