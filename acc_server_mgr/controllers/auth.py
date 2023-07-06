import logging

import jwt
import pydantic
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError

from acc_server_mgr.controllers.utils import Unauthorized, Forbidden
from acc_server_mgr.database import use_db
from acc_server_mgr.storage import user as storage

router = APIRouter(prefix="/auth", tags=["auth"])
secret = "secret"
algorithm = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
log = logging.getLogger(__name__)


def require_auth(token=Depends(oauth2_scheme)):
    try:
        return jwt.decode(token.encode("UTF-8"), secret, algorithms=[algorithm])
    except PyJWTError as err:
        log.exception("token decode error")
        raise Forbidden()


class TokenResponse(pydantic.BaseModel):
    token_type: str
    access_token: str
    scope: str


def _jwt_encode(user_obj):
    return jwt.encode({
        "user_id": user_obj.id,
        "user_mail": user_obj.mail,
        "scopes": user_obj.scopes
    }, secret, algorithm=algorithm)


@router.post("/token", response_model=TokenResponse)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(use_db)):
    user_obj = storage.find_by_credentials(db, form_data)
    if user_obj is None:
        raise Unauthorized()
    return TokenResponse(
        token_type="bearer",
        access_token=_jwt_encode(user_obj),
        scope=user_obj.scopes
    )


@router.post("/token-check")
def token_check(request: Request, db=Depends(use_db), token=Depends(require_auth)):
    user_obj = storage.get_one_by(db, id=token["user_id"], mail=token["user_mail"])
    if user_obj is None:
        raise Unauthorized()
    return {
        "status": "authenticated",
        "access_token": _jwt_encode(user_obj)
    }

