from datetime import datetime
from typing import Optional

from peewee import prefetch

from acc_server_mgr.storage.utils import apply_filter, apply_sort
from acc_server_mgr.models.db import (
    Event as EventModel,
    Session as SessionModel,
)
from acc_server_mgr.models.schema import (
    FilterRequest, EventCreateRequest, EventUpdateRequest,
)


def _load_event(_id):
    event_query = EventModel.select(EventModel).where(EventModel.id == _id).limit(1)
    session_query = SessionModel.select(SessionModel)
    results = prefetch(event_query, session_query)
    for result in results:
        return result


def create_one(db, data: EventCreateRequest) -> EventModel:
    with db:
        event_data = data.dict(exclude_unset=True)
        event_data.pop("sessions")
        event_obj = EventModel(**event_data, created=datetime.now())
        event_obj.save()
        for session in data.sessions:
            SessionModel(
                **session.dict(exclude_unset=True),
                event=event_obj,
                created=datetime.now()
            ).save()
        return event_obj


def get_one(db, _id: int) -> Optional[EventModel]:
    with db:
        return _load_event(_id)


def update_one(db, _id: int, data: EventUpdateRequest) -> Optional[EventModel]:
    with db:
        obj = _load_event(_id)
        if obj is None:
            return None

        event_data = data.dict(exclude_unset=True)
        event_data.pop("sessions")
        for attr, value in event_data.items():
            setattr(obj, attr, value)

        updated_session_ids = []

        for session in data.sessions:
            if session.id is not None:
                updated_session_ids.append(session.id)
            SessionModel(
                **session.dict(exclude_unset=True),
                event=obj,
                created=datetime.now()
            ).save()


        for session in obj.sessions:
            if session.id not in updated_session_ids:
                session.delete_instance()

        obj.save()
        return _load_event(obj.id)


def delete_one(db, _id: int):
    with db:
        SessionModel.delete().where(SessionModel.event_id == _id)
        EventModel.delete().where(EventModel.id == _id)


def search(db, filter_: FilterRequest):
    with db:
        event_query = EventModel.select(EventModel)
        session_query = SessionModel.select(SessionModel)
        event_query = apply_filter(event_query, EventModel, filter_)
        event_query = apply_sort(event_query, EventModel, filter_)
        return event_query.count(), prefetch(
            event_query.paginate(filter_.page, filter_.items_per_page),
            session_query
        )
