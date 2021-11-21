from fastapi.encoders import jsonable_encoder

from constant import ALLOWED_EXTENSIONS


def validate_file_extension(fn):
    """
    Validate file extension.
    """
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def build_response(status: bool = True, data=None):
    return jsonable_encoder({
        'status': status,
        'data': data
    }, exclude_none=True)
