from http.client import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request", code: int = 400):
        self.detail = detail
        self.code = code
        self.status_code = 400
        super().__init__()


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found", code: int = 404):
        self.detail = detail
        self.code = code
        self.status_code = 404
        super().__init__()

class UnexpectedServerException(HTTPException):
    def __init__(self, detail: str = "Unexpected server exception", code: int = 500):
        self.detail = detail
        self.code = code
        self.status_code = 500
        super().__init__()

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden", code: int = 401):
        self.detail = detail
        self.code = code
        self.status_code = 401
        super().__init__()