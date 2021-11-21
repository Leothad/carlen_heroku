from fastapi.encoders import jsonable_encoder


class Error():
    message: str
    status_code: int

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
