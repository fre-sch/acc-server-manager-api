from peewee import TextField, BooleanField, DateTimeField, IntegerField, \
    FloatField, ForeignKeyField

from acc_server_mgr.database import Base


class User(Base):
    mail = TextField()
    password_hash = TextField()
    is_enabled = BooleanField()
    created = DateTimeField()
    last_login = DateTimeField(null=True)
    scopes = TextField(null=True)


class Configuration(Base):
    created = DateTimeField()
    name = TextField()
    tcp_port = IntegerField()
    udp_port = IntegerField()
    register_to_lobby = BooleanField()
    max_connections = IntegerField()
    lan_discovery = BooleanField()
    config_version = TextField()
    public_ip = TextField()


class Settings(Base):
    created = DateTimeField()
    server_name = TextField()
    admin_password = TextField()
    car_group = TextField()
    track_medals_requirement = IntegerField()
    safety_rating_requirement = IntegerField()
    racecraft_rating_requirement = IntegerField()
    password = TextField()
    spectator_password = TextField()
    max_car_slots = IntegerField()
    dump_leaderboards = BooleanField()
    dump_entry_list = BooleanField()
    is_race_locked = BooleanField()
    short_formation_lap = BooleanField()
    formation_lap_type = IntegerField()
    do_driver_swap_broadcast = BooleanField()
    randomize_track_when_empty = BooleanField()
    central_entry_list_path = TextField()
    allow_auto_dq = BooleanField()
    ignore_premature_disconnects = BooleanField()
    config_version = TextField()


class Event(Base):
    created = DateTimeField()
    name = TextField()
    track = TextField()
    pre_race_waiting_time_seconds = IntegerField()
    session_over_time_seconds = IntegerField()
    ambient_temp = IntegerField()
    cloud_level = FloatField()
    rain = FloatField()
    weather_randomness = IntegerField()
    post_qualy_seconds = IntegerField()
    post_race_seconds = IntegerField()
    meta_data = TextField()
    simracer_weather_conditions = BooleanField()
    is_fixed_condition_qualification = BooleanField()


class Session(Base):
    created = DateTimeField()
    name = TextField()
    hour_of_day = IntegerField()
    day_of_weekend = IntegerField()
    time_multiplier = IntegerField()
    session_type = TextField()
    session_duration_minutes = IntegerField()
    event = ForeignKeyField(Event, backref="sessions")


class ServerConfig(Base):
    created = DateTimeField()
    name = TextField()
    configuration = ForeignKeyField(Configuration)
    settings = ForeignKeyField(Settings)
    event = ForeignKeyField(Event)
    is_enabled = BooleanField()
    is_running = BooleanField()
    last_start = DateTimeField()
    last_stop = DateTimeField()
    process_id = IntegerField()
