from starlette.exceptions import HTTPException


def authorize(token, *required_scopes):
    if token["scopes"] is None:
        raise Forbidden()

    if "admin" in token["scopes"]:
        return

    for scope in required_scopes:
        if scope not in token["scopes"]:
            raise Forbidden()


class NotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404)


class Unauthorized(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)


class Forbidden(HTTPException):
    def __init__(self):
        super().__init__(status_code=403)



