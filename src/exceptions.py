from fastapi import HTTPException


# BaseExceptions
class ReservationServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ReservationServiceException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(ReservationServiceException):
    detail = "Объект уже существует"


class TableNotFoundException(ObjectNotFoundException):
    detail = "Стол не найден"


class ReservationNotFoundException(ObjectNotFoundException):
    detail = "Бронирование не найдено"


class ReservationAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Стол уже забронирован на данное время"


class KeyIsStillReferencedException(ReservationServiceException):
    detail = "Ключ все еще используется"


class TableKeyIsStillReferencedException(ReservationServiceException):
    detail = "Ключ стола все еще используется"


# HTTPExceptions
class ReservationServiceHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TableNotFoundHTTPException(ReservationServiceHTTPException):
    status_code = 404
    detail = "Стол не найден"


class ReservationNotFoundHTTPException(ReservationServiceHTTPException):
    status_code = 404
    detail = "Бронирование не найдено"


class ReservationAlreadyExistsHTTPException(ReservationServiceHTTPException):
    status_code = 409
    detail = "Стол уже забронирован на данное время"


class TableKeyIsStillReferencedHTTPException(ReservationServiceHTTPException):
    status_code = 409
    detail = "Ключ стола все еще используется в другой таблице"
   