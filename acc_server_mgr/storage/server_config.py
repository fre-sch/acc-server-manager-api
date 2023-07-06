from datetime import datetime

from acc_server_mgr.storage.utils import apply_filter
from acc_server_mgr.models.schema import (
    ServerConfig,
    ServerConfigUpdate, FilterRequest,
)
from acc_server_mgr.models.db import ServerConfig as ServerConfigModel


def create_one(db, data: ServerConfig) -> ServerConfigModel:
    with db:
        obj = ServerConfigModel(
            **data.dict(),
            created=datetime.now()
        )
        obj.save()
        return obj


def get_one(db, _id: int) -> ServerConfigModel:
    with db:
        return ServerConfigModel.get_or_none(ServerConfigModel.id == _id)


def update_one(db, _id: int, data: ServerConfigUpdate) -> ServerConfigModel:
    with db:
        obj = ServerConfigModel.get_or_none(ServerConfigModel.id == _id)
        if obj:
            for attr, value in data.dict().items():
                setattr(obj, attr, value)
        return obj


def delete_one(db, _id: int):
    with db:
        ServerConfigModel.delete().where(ServerConfigModel.id == _id)


def search(db, filter_: FilterRequest):
    with db:
        query = ServerConfigModel.select()
        apply_filter(query, ServerConfigModel, filter_)
        return query.count(), list(query)


def update_obj(db, obj: ServerConfigModel):
    with db:
        obj.save()
        return obj
