from fastapi import HTTPException, status

not_found_api_lambda_key = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="API Key not found",
)

invalid_api_lambda_key = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid API Key",
)