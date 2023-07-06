from acc_server_mgr.database import db
from acc_server_mgr.models import schema
from acc_server_mgr.models.db import (
    User,
    Configuration,
    Settings,
    Event,
    Session,
    ServerConfig,
)
from acc_server_mgr.storage import user


if __name__ == "__main__":
    with db:
        db.create_tables([
            User, Configuration, Settings, Event, Session, ServerConfig,
        ])
        user.create_one(db, schema.UserCreate(
            mail="admin@test.local",
            password="password",
            scopes="admin",
            is_enabled=True,
        ))
