from http import HTTPStatus


class AppError(Exception):
    def __init__(self, reason: str, status: HTTPStatus):
        super().__init__(f'[{status}] {reason}')
        self.reason = reason
        self.status = status


class ConflictError(AppError):
    def __init__(self, entity: str):
        super().__init__(f'cannot add {entity}', HTTPStatus.CONFLICT)
        self.entity = entity


class NotFoundError(AppError):
    def __init__(self, entity: str):
        super().__init__(f'cannot find {entity}', HTTPStatus.NOT_FOUND)
        self.entity = entity


class RequestNotContainError(AppError):
    def __init__(self, entity: str):
        super().__init__(f'Request should contain {entity}', HTTPStatus.BAD_REQUEST)
        self.entity = entity


class NotAcceptableError(AppError):
    def __init__(self, entity: str):
        super().__init__(f'Request contain not acceptable {entity}', HTTPStatus.BAD_REQUEST)
        self.entity = entity
