from fastapi import Request
from app.exception import not_found_api_lambda_key, invalid_api_lambda_key

def valid_header(request:Request, api_key:str) -> Request:
    flag_aux = request.headers.get("API-LAMBDA-KEY")
    if flag_aux is None:
        raise not_found_api_lambda_key
    if flag_aux == api_key:
        return request
    else:
        raise invalid_api_lambda_key
    