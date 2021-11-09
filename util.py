from constant import ALLOWED_EXTENSIONS


def validate_file_extension(fn):
    """
    Validate file extension.
    """
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
