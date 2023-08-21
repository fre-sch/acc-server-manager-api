from fastapi import APIRouter, Depends, Response
from acc_server_mgr import process_control
from acc_server_mgr.controllers.auth import require_auth
from acc_server_mgr.controllers.utils import authorize, NotFound
from acc_server_mgr.database import use_db
from acc_server_mgr.models.schema import (
    ServerConfig,
    ServerConfigCreate,
    ServerConfigUpdate,
    ServerConfigResponse, ServerConfigSearchResponse, FilterRequest,
)
from acc_server_mgr.storage import server_config as storage


AUTH_SCOPE = "server_config"
router = APIRouter(prefix="/server_config", tags=["server_config"])


@router.post("/", response_model=ServerConfigResponse)
def create(data: ServerConfigCreate, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    obj = storage.create_one(db, data)
    return ServerConfigResponse.from_orm(obj)


@router.get("/{id}", response_model=ServerConfigResponse)
def get_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    obj = storage.get_one(db, id)
    if obj:
        return ServerConfigResponse.from_orm(obj)

    raise NotFound()


@router.patch("/{id}", response_model=ServerConfigResponse)
def update_one(id: int,
               data: ServerConfigUpdate,
               auth=Depends(require_auth),
               db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    updated_server_config = storage.update_one(db, id, data)
    if updated_server_config:
        return ServerConfigResponse.from_orm(updated_server_config)

    raise NotFound()


@router.delete("/{id}")
def delete_one(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    storage.delete_one(db, id)
    return Response(status_code=204)


@router.post("/_filter", response_model=ServerConfigSearchResponse)
def filter_(filter_request: FilterRequest,
            auth=Depends(require_auth),
            db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    count, items = storage.search(db, filter_request)
    return ServerConfigSearchResponse(
        total_count=count,
        items=[ServerConfigResponse.from_orm(it) for it in items]
    )


@router.post("/{id}/_start", response_model=ServerConfigResponse)
def start(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    server_config = storage.get_one(db, id)

    if server_config is None:
        raise NotFound()

    try:
        process_control.start_server(server_config)
        storage.update_obj(server_config)
    except Exception:
        pass

    return ServerConfigResponse.from_orm(server_config)


@router.post("/{id}/_stop", response_model=ServerConfigResponse)
def stop(id: int, auth=Depends(require_auth), db=Depends(use_db)):
    """
    requires user authorization scope ``server_config``
    """
    authorize(auth, AUTH_SCOPE)
    server_config = storage.get_one(db, id)
    if server_config is None:
        raise NotFound()

    try:
        process_control.stop_server(server_config)
        storage.update_obj(db, server_config)
    except Exception:
        pass

    return ServerConfigResponse.from_orm(server_config)
