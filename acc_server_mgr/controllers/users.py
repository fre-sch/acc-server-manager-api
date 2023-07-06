from fastapi import APIRouter, Response, Depends
from acc_server_mgr.controllers.auth import require_auth
from acc_server_mgr.controllers.utils import NotFound, authorize
from acc_server_mgr.database import use_db
from acc_server_mgr.models.schema import UserCreate, UserUpdate, UserResponse, \
    UserFilterResponse, FilterRequest
from acc_server_mgr.storage import user as storage


AUTH_SCOPE = "user"
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, auth=Depends(require_auth), db=Depends(use_db)):
    authorize(auth, AUTH_SCOPE)
    new_user = storage.create_one(db, user)
    return UserResponse.from_orm(new_user)


@router.get("/{id}", response_model=UserResponse)
def get_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    authorize(auth, AUTH_SCOPE)
    user = storage.get_one(db, id)
    if user:
        return UserResponse.from_orm(user)

    raise NotFound()


@router.patch("/{id}", response_model=UserResponse)
def update_one(id: int, user: UserUpdate, auth=Depends(require_auth), db=Depends(use_db)):
    authorize(auth, AUTH_SCOPE)
    updated_user = storage.update_one(db, id, user)
    if updated_user:
        return UserResponse.from_orm(updated_user)

    raise NotFound()


@router.delete("/{id}")
def delete_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    authorize(auth, AUTH_SCOPE)
    storage.delete_one(db, id)
    return Response(status_code=204)


@router.post("/_filter", response_model=UserFilterResponse)
def filter_(filter_request: FilterRequest, auth=Depends(require_auth), db=Depends(use_db)):
    authorize(auth, AUTH_SCOPE)
    total_count, items = storage.search(db, filter_request)
    return UserFilterResponse(
        total_count=total_count,
        items=[UserResponse.from_orm(it) for it in items]
    )
