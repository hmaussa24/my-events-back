from fastapi import HTTPException, status

class CustomException(HTTPException):
    pass