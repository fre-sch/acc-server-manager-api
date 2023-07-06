from fastapi import APIRouter, Depends, Response
from acc_server_mgr.controllers.auth import require_auth
from acc_server_mgr.controllers.utils import authorize, NotFound
from acc_server_mgr.database import use_db
from acc_server_mgr.models.schema import (
    Event,
    EventUpdateRequest,
    EventCreateRequest,
    EventResponse,
    EventSearchResponse, FilterRequest,
)
from acc_server_mgr.storage import event as storage

AUTH_SCOPE = "event"

router = APIRouter(prefix="/event", tags=["event"])


@router.post("/", response_model=EventResponse)
def create(data: EventCreateRequest, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``event``
    """
    authorize(auth, AUTH_SCOPE)
    obj = storage.create_one(db, data)
    return EventResponse.from_orm(obj)


@router.get("/{id}", response_model=EventResponse)
def get_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``event``
    """
    authorize(auth, AUTH_SCOPE)
    obj = storage.get_one(db, id)
    if obj:
        return EventResponse.from_orm(obj)

    raise NotFound()


@router.patch("/{id}", response_model=EventResponse)
def update_one(id: int,
               data: EventUpdateRequest,
               auth=Depends(require_auth),
               db=Depends(use_db)):
    """
    requires user authorization scope ``event``
    """
    authorize(auth, AUTH_SCOPE)
    update_obj = storage.update_one(db, id, data)
    if update_obj:
        return EventResponse.from_orm(update_obj)

    raise NotFound()


@router.delete("/{id}")
def delete_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``event``
    """
    authorize(auth, AUTH_SCOPE)
    storage.delete_one(db, id)
    return Response(status_code=204)


@router.post("/_filter", response_model=EventSearchResponse)
def filter_(filter_request: FilterRequest,
            auth=Depends(require_auth),
            db=Depends(use_db)):
    """
    requires user authorization scope ``event``
    """
    authorize(auth, AUTH_SCOPE)
    count, items = storage.search(db, filter_request)
    return EventSearchResponse(
        total_count=count,
        items=[EventResponse.from_orm(it) for it in items]
    )
