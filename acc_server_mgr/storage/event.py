from datetime import datetime

from peewee import JOIN, prefetch

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
        return _load_event(event_obj.id)


def get_one(db, _id: int) -> EventModel:
    with db:
        return _load_event(_id)


def update_one(db, _id: int, data: EventUpdateRequest) -> EventModel:
    with db:
        obj = _load_event(_id)
        if obj:
            _attrs = data.dict(exclude_unset=True)
            for attr, value in _attrs.items():
                setattr(obj, attr, value)
            obj.save()
        return obj


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
