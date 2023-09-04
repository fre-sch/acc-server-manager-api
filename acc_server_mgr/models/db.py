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
    name = TextField()
    created = DateTimeField()
    is_enabled = BooleanField()
    event = ForeignKeyField(Event, null=True)

    ## settings.json
    settings_server_name = TextField()
    settings_admin_password = TextField()
    settings_car_group = TextField()
    settings_track_medals_requirement = IntegerField()
    settings_safety_rating_requirement = IntegerField()
    settings_racecraft_rating_requirement = IntegerField()
    settings_password = TextField()
    settings_spectator_password = TextField()
    settings_max_car_slots = IntegerField()
    settings_dump_leaderboards = BooleanField()
    settings_dump_entry_list = BooleanField()
    settings_is_race_locked = BooleanField()
    settings_short_formation_lap = BooleanField()
    settings_formation_lap_type = IntegerField()
    settings_do_driver_swap_broadcast = BooleanField()
    settings_randomize_track_when_empty = BooleanField()
    settings_central_entry_list_path = TextField()
    settings_allow_auto_dq = BooleanField()
    settings_ignore_premature_disconnects = BooleanField()
    settings_version = TextField()

    ## config.json
    config_tcp_port = IntegerField()
    config_udp_port = IntegerField()
    config_register_to_lobby = BooleanField()
    config_max_connections = IntegerField()
    config_lan_discovery = BooleanField()
    config_version = TextField()
    config_public_ip = TextField()

    ## runtime house keeping
    process_is_running = BooleanField(default=False)
    process_last_start = DateTimeField(null=True)
    process_last_stop = DateTimeField(null=True)
    process_id = IntegerField(null=True)
