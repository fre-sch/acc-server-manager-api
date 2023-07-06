from datetime import datetime

from acc_server_mgr.storage.utils import apply_filter, apply_sort
from acc_server_mgr.models.db import Configuration as ConfigurationModel
from acc_server_mgr.models.schema import (
    Configuration, FilterRequest
)


def create_one(db, data: Configuration) -> ConfigurationModel:
    with db:
        obj = ConfigurationModel(**data.dict(), created=datetime.now())
        obj.save()
        return obj


def get_one(db, _id: int) -> ConfigurationModel:
    with db:
        return ConfigurationModel.get_or_none(ConfigurationModel.id == _id)


def update_one(db, _id: int, data: Configuration) -> ConfigurationModel:
    with db:
        obj = ConfigurationModel.get_or_none(ConfigurationModel.id == _id)
        if obj:
            _attrs = data.dict(exclude_unset=True)
            for attr, value in _attrs.items():
                setattr(obj, attr, value)
            obj.save()
        return obj


def delete_one(db, _id: int):
    with db:
        ConfigurationModel.delete().where(ConfigurationModel.id == _id)


def search(db, filter_: FilterRequest):
    with db:
        query = ConfigurationModel.select(ConfigurationModel)
        query = apply_filter(query, ConfigurationModel, filter_)
        query = apply_sort(query, ConfigurationModel, filter_)
        return query.count(), list(query)
