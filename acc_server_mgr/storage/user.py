import logging
from datetime import datetime
from hashlib import sha512

from acc_server_mgr.storage.utils import apply_filter
from acc_server_mgr.models.schema import UserCreate, UserUpdate, FilterRequest
from acc_server_mgr.models.db import User as UserModel


log = logging.getLogger(__name__)


def hash_password(value):
    return sha512(value.encode("UTF-8")).hexdigest()


def create_one(db, user: UserCreate) -> UserModel:
    with db:
        data = user.dict()
        data["password_hash"] = hash_password(data.pop("password"))
        new_user = UserModel(**data, created=datetime.now())
        new_user.save()
        return new_user


def get_one(db, _id: int) -> UserModel:
    with db:
        return UserModel.get_or_none(UserModel.id == _id)


def get_one_by(db, **kwargs):
    with db:
        return UserModel.get_or_none(**kwargs)


def update_one(db, _id: int, user: UserUpdate) -> UserModel:
    with db:
        user_obj = UserModel.get_or_none(UserModel.id == _id)
        if user_obj:
            data = user.dict()
            if "password" in data:
                data["password_hash"] = hash_password(data.pop("password"))
            for attr, value in data.items():
                setattr(user_obj, attr, value)
            user_obj.save()
        return user_obj


def delete_one(db, _id: int):
    with db:
        UserModel.delete().where(UserModel.id == _id)


def find_by_credentials(db, credentials) -> UserModel:
    with db:
        password_hash = hash_password(credentials.password)
        query = UserModel.select().where(
            (UserModel.mail == credentials.username)
            & (UserModel.password_hash == password_hash)
        ).limit(1)
        user_obj = query.first()
        if user_obj:
            user_obj.last_login = datetime.now()
            user_obj.save()
            return user_obj


def search(db, filter_: FilterRequest) -> tuple[int, list[UserModel]]:
    with db:
        query = UserModel.select()
        query = apply_filter(query, UserModel, filter_)
        return query.count(), list(query)
