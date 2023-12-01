from fastapi import APIRouter, Request, status, UploadFile
from typing import Union
from app.security import valid_header
from app.config import API_KEY, SEND_GS, URL_SENDER_GS

from app.payments.utils import (
    process_uploaded_file,
    select_bank,
    get_bank_data
)
import requests

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/upload_payment_file", status_code=status.HTTP_201_CREATED)
async def upload_payment_file(file: Union[UploadFile, None], request: Request):
    try:
        valid_header(request, API_KEY)
        if not file:
            return {"message": "No file uploaded"}
        result_list = process_uploaded_file(file)
        print(result_list)
        banks = ["INTERBANK", "BBVA", "SCOTIABANK", "BANBIF"]
        selection = select_bank(result_list, banks)
        print(selection)
        matches_dict = get_bank_data(selection, result_list)
        print(matches_dict)
        to_send = SEND_GS == "True"
        if to_send:
            data_payment = {
                "date_payment": "2021-09-01",
                "dni": matches_dict.get("DNI", ""),
                "total": matches_dict.get("Total", ""),
                "bank": matches_dict.get("Banco", ""),
                "mode_payment": "DS",
                "operation_code": matches_dict.get("Codigo de operacion", ""),
                "card_number": matches_dict.get("Numero tarjeta", "")
            }
            res = requests.post(URL_SENDER_GS, json=data_payment)
            if res.status_code != 201:
                return {"message": "Error sending data to google sheet"}
            return {'mensaje': 'Imagen subida satisfactoriamente', 'datos': matches_dict}
    except Exception as e:
         return {'message': 'An error occurred', 'error': str(e)}