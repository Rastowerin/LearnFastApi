class BadRequestError(Exception):
    @property
    def status(self):
        raise NotImplemented


class UserNotFoundException(BadRequestError):
    status = 404


class InvalidCredentialsException(BadRequestError):
    status = 400


class UserAlreadyExistsException(BadRequestError):
    status = 409
