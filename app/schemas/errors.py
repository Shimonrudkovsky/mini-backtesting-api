from fastapi import HTTPException


class DataNotFoundException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "No data was found"


class StorageError(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Something wrong with the storage"
