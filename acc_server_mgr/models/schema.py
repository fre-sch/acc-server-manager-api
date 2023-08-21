from datetime import datetime
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field, validator
from pydantic.types import Any, conint, confloat

from acc_server_mgr.models.utils import AllOptional


class BaseModel(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat(timespec="seconds")}


class FilterOperator(str, Enum):
    eq = "=="
    neq = "!="
    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="
    contains = "contains"


FilterTerm = tuple[str, FilterOperator, Any]


class SortingDir(str, Enum):
    asc = "asc"
    desc = "desc"


SortTerm = tuple[str, SortingDir]


class FilterRequest(BaseModel):
    query: list[FilterTerm]
    sort: list[SortTerm]
    page: Optional[int] = 0
    items_per_page: Optional[int] = 10


class UserCredentials(BaseModel):
    mail: str
    password: str


class UserCreate(BaseModel):
    mail: str
    password: str = Field(..., view="password")
    password_confirm: str = Field(..., view="password")
    scopes: str = Field(
        ...,
        description="Entities and actions can this user can access and perform",
        # TODO: use format (impl in API and SPA)
        pattern="^[a-zA-Z0-9_-][,a-zA-Z0-9_-]*$",
        view="csv"
    )
    is_enabled: bool = Field(
        ...,
        description="enabled users can login, disabled users cannot"
    )


class UserUpdate(BaseModel):
    mail: str = None
    password: str = Field(None,
                          description="Filling this out will change the password",
                          view="password")
    password_confirm: str = Field(None, description="Filling this out will change the password", view="password")
    is_enabled: bool = Field(
        None,
        description="enabled users can login, disabled users cannot"
    )
    scopes: str = Field(
        None,
        description="Entities and actions can this user can access and perform",
        # TODO: use format (impl in API and SPA)
        pattern="^[a-zA-Z0-9_-][,a-zA-Z0-9_-]*$",
        view="csv"
    )
    created: datetime = Field(None, view="view-only")
    last_login: datetime = Field(None, view="view-only")


class UserResponse(BaseModel):
    id: int
    mail: str
    is_enabled: bool
    created: datetime
    last_login: Optional[datetime]
    scopes: str


class UserFilterResponse(BaseModel):
    total_count: int
    items: list[UserResponse]


class UserTokenRequest(BaseModel):
    access_token: str


class Session(BaseModel):
    """
    Properties of an event session. Included as part of `event.json`.
    """

    name: str
    hour_of_day: int = Field(
        ...,
        alias="hourOfDay",
        description=(
            "Session starting hour of the day, values 0, 1, 2 ... 22, 23"
        ),
    )
    day_of_weekend: int = Field(
        ...,
        alias="dayOfWeekend",
        description="Race weekend day, 1 = Friday, 2 = Saturday, 3 = Sunday",
    )
    time_multiplier: int = Field(
        ...,
        alias="timeMultiplier",
        description=(
            "Rate at which the session time advances in realtime. Values 0, 1,"
            " ... 24"
        ),
    )
    session_type: str = Field(
        ...,
        alias="sessionType",
        description="Race session type: P = Practice, Q = Qualifying, R = Race",
        enum=["P", "Q", "R"],
    )
    session_duration_minutes: int = Field(
        ...,
        alias="sessionDurationMinutes",
        description="Session duration in minutes",
    )


class SessionResponse(Session):
    id: int


class Event(BaseModel):
    """
    Environment conditions for races. Used to create `event.json` of server
    instances.
    """

    name: str
    created: datetime = Field(..., step=1)
    track: str = Field(
        ...,
        description=(
            "Track server is running. Setting a wrong value will also  print"
            " out the available track keys in the log. With the 1.1 update"
            " containing the 2019 season content, each track has a _2019"
            " variant. Using this track will set the BoP and track grip"
            " correspondingly."
        ),
    )
    pre_race_waiting_time_seconds: conint(ge=30, multiple_of=1) = Field(
        ...,
        alias="preRaceWaitingTimeSeconds",
        description="Preparation time before a race. Cannot be less than 30s.",
    )
    session_over_time_seconds: conint(ge=0, multiple_of=1) = Field(
        ...,
        alias="sessionOverTimeSeconds",
        description=(
            "Time after that a session is forcibly closing after the timer"
            " reached '0:00. Something like 107% of the expected laptime is"
            " recommended. Careful: default 2 minutes does not properly cover"
            " tracks like Spa or Silverstone."
        ),
    )
    ambient_temp: int = Field(
        ...,
        alias="ambientTemp",
        description="Sets the baseline ambient temperature in °C.",
    )
    cloud_level: confloat(ge=0, le=1, multiple_of=0.1) = Field(
        ...,
        alias="cloudLevel",
        description=(
            "Sets the baseline cloud level, →Race Weekend Simulation. Values"
            " 0.0, 0.1, .... 1.0"
        ),
    )
    rain: confloat(ge=0, le=1, multiple_of=0.1) = Field(
        ...,
        description=(
            "If weather randomness is off, defines the static rain level. With"
            " dynamic weather, it increases the rain chance. 0.0 = dry, 0.2"
            " light rain, 0.5 rain, 0.7 heavy rain, 1.0 very heavy. Values"
            " greater than 0.1 can override the value of cloudLevel."
        ),
    )
    weather_randomness: conint(ge=0, multiple_of=1) = Field(
        ...,
        alias="weatherRandomness",
        description=(
            "Sets the dynamic weather level: 0 = static weather, 1 - 4 = fairly"
            " realistic weather, 5 - 7 = more sensational."
        ),
    )
    post_qualy_seconds: int = Field(
        ...,
        alias="postQualySeconds",
        description=(
            "The time after the last driver is finished (or the"
            " sessionOverTimeSeconds passed) in Q sessions and the race start."
            " Should not be set to 0, otherwise grid spawning is not secure."
        ),
    )
    post_race_seconds: int = Field(
        ...,
        alias="postRaceSeconds",
        description=(
            "Additional time after the race ended for everyone, before the next"
            " race weekend starts."
        ),
    )
    meta_data: str = Field(
        ...,
        alias="metaData",
        description=(
            "A user-defined string that will be transferred to the result"
            " outputs."
        ),
    )
    simracer_weather_conditions: bool = Field(
        ...,
        alias="simracerWeatherConditions",
        description=(
            "Experimental / not supported: if set to true, this will limit the"
            " maximum rain/wetness to roughly 2/3 of the maximum values,"
            " translating to something between medium and heavy rain. It may be"
            " useful if you feel forced to run very low cloudLevel and"
            " weatherRandomness values just to avoid thunderstorm; however,"
            " high levels (0.4+ clouds combined with 5+ randomness) will still"
            " result in quite serious conditions."
        ),
    )
    is_fixed_condition_qualification: bool = Field(
        ...,
        alias="isFixedConditionQualification",
        description=(
            "Experimental / not supported: if set to true, the server will take"
            " the rain, cloud, temperature, rain levels literally and make sure"
            " whatever is set up never changes. Daytime transitions still"
            " happen visually, but do not affect the temperatures or road"
            " wetness. Also rubber/grip is always the same. This is intended to"
            " be used for private league qualification servers only."
        ),
    )


class EventCreateRequest(Event):
    created: Optional[datetime] = Field(..., step=1)
    sessions: list[Session]


class EventUpdateRequest(Event, metaclass=AllOptional):
    sessions: list[Session]


class EventResponse(Event):
    id: int
    sessions: list[SessionResponse]

    _sessions_list = validator("sessions", pre=True, allow_reuse=True)(list)


class EventSearchResponse(BaseModel):
    total_count: int
    items: list[EventResponse]


class ServerConfig(BaseModel):
    """
    Configuration of instances of a server process.
    """

    name: str
    created: datetime
    event_id: int
    is_enabled: bool = Field(
        ...,
        description="Can be started and stopped"
    )

    ## settings.json
    settings_server_name: str = Field(
        ...,
        description="The server name displayed in the ACC UI pages",
    )
    settings_admin_password: str = Field(
        ...,
        description=(
            "The password you specify allows a driver or spectator to log in as"
            " Server Admin in the chat window ( ENTER key ) of the server."
        ),
    )
    settings_car_group: str = Field(
        ...,
        enum=["FreeForAll", "GT3", "GT4", "GTC"],
        description=(
            "Defines the car group for this server. Possible values are"
            " FreeForAll, GT3, GT4, GTC."
        ),
    )
    settings_track_medals_requirement: int = Field(
        ...,
        enum=[0, 1, 2, 3],
        description=(
            "Defines the amount of track medals that a user has to have for the"
            " given track. Values: 0, 1, 2, 3."
        ),
    )
    settings_safety_rating_requirement: int = Field(
        ...,
        description=(
            "Defines the Safety Rating (SA) that a user must have to join this"
            " server. Values: -1, 0, 1, 2, 3, 4, .... 97, 98, 99."
        ),
    )
    settings_racecraft_rating_requirement: int = Field(
        ...,
        description=(
            "Defines the Racecraft Rating (RC) that a user must have to join"
            " this server. Values: -1, 0, 1, 2, 3, 4, .... 97, 98, 99."
        ),
    )
    settings_password: str = Field(
        ...,
        description=(
            "Password required to enter this server. If a password is set, the"
            " server is declared Private Multiplayer."
        ),
    )
    settings_spectator_password: str = Field(
        ...,
        description=(
            "Password to enter the server as a spectator. Must be different"
            " from 'password' if both are set."
        ),
    )
    settings_max_car_slots: int = Field(
        ...,
        description=(
            "Defines the amount of car slots the server can occupy; this value"
            " is overridden if the pit count of the track is lower, or with 30"
            " for public MP. The gap between maxCarSlots and maxConnections (in"
            " configuration.json) defines how many spectators or other"
            " irregular connections (ie entry list entries) can be on the"
            " server."
        ),
    )
    settings_dump_leaderboards: bool = Field(
        ...,
        description=(
            "If set to true, any session will write down the result leaderboard"
            " in a 'results' folder (must be manually created)."
        ),
    )
    settings_dump_entry_list: bool = Field(
        ...,
        description=(
            "Will save an entry list at the end of any Qualifying session. This"
            " can be a quick way to collect a starting point to build an entry"
            " list and is a way to save the defaultGridPositions which can be"
            " used to run a race without Qualifying session and predefined"
            " grid. Also see the corresponding admin command."
        ),
    )
    settings_is_race_locked: bool = Field(
        ...,
        description=(
            "If set to false, the server will allow joining during a race"
            " session. Is not useful in →Public Multiplayer, as the user-server"
            " matching will ignore ongoing race sessions."
        ),
    )
    settings_short_formation_lap: bool = Field(
        ...,
        description=(
            "False = one formation lap - Useful for Private Multiplayer. True ="
            " short formation lap."
        ),
    )
    settings_formation_lap_type: int = Field(
        ...,
        enum=[0, 1, 3, 4, 5],
        description=(
            "Toggles the formation lap type that is permanently used on this"
            " server: 5 = short formation lap with position control and UI + 1"
            " ghosted cars lap, 4 = one free formation lap + 1 ghosted cars"
            " lap, 3 = default formation lap with position control and UI, 1 ="
            " old limiter lap, 0 = free (replaces /manual start), only usable"
            " for private servers."
        ),
    )
    settings_do_driver_swap_broadcast: bool = Field(
        ...,
    )
    settings_randomize_track_when_empty: bool = Field(
        ...,
        description=(
            "If set to true, the server will change to a random track when the"
            " last driver leaves (which causes a reset to FP1). The 'track'"
            " property will only define the default state for the first"
            " session."
        ),
    )
    settings_central_entry_list_path: str = Field(
        ...,
        description=(
            "Can override the default entryList path 'cfg/entrylist.json', so"
            " multiple ACC servers on the machine can use the same entry list"
            " (and custom car files). Set a full path like"
            " 'C:/customEntryListSeriesA/', where the entry list is stored."
            " Attention: The path separators have to be slashes (/),"
            " backslashes (\\) will not work."
        ),
    )
    settings_allow_auto_dq: bool = Field(
        ...,
        description=(
            "If set to false, the server won't automatically disqualify drivers"
            " and instead hand out Stop&Go (30 Seconds) penalties. This way, a"
            " server admin / race director has 3 laps time to review the"
            " incident and either use /dq or /clear based on his judgment."
        ),
    )
    settings_ignore_premature_disconnects: bool = Field(
        ...,
        description=(
            "Removes a (very good) fix where users can randomly lose the"
            " connection. There is no sane reason to turn this off. 1 ="
            " default: less arbitrary connections lost, 0 = more timeouts, but"
            " strict disconnection of anyone who appears inactive for 5"
            " seconds. Can be useful on unsupported platforms where TCP sockets"
            " act differently."
        ),
    )
    settings_version: str

    ## config.json
    config_tcp_port: int = Field(
        ...,
        description=(
            "ACC clients will use this port to establish a connection to the"
            " server"
        ),
    )
    config_udp_port: int = Field(
        ...,
        description=(
            "Connected clients will use this port to stream the car positions"
            " and is used for the ping test. In case you never see your server"
            " getting a ping value, this indicates that the udpPort is not"
            " accessible"
        ),
    )
    config_register_to_lobby: bool = Field(
        ...,
        description=(
            "Indicates whether the server should register to the backend. True:"
            " The server is declared as Public Multiplayer. False: The server"
            " is declared as Private Multiplayer. Useful for LAN sessions."
        ),
    )
    config_max_connections: int = Field(
        ...,
        description=(
            "The maximum amount of connections a server will accept at a time."
            " If you own the hardware server, you can just set any high number"
            " you want. If you rented a 16 or 24 slot server, your Hosting"
            " Provider probably has set this here and doesn't give you"
            " write-access to this configuration file."
        ),
    )
    config_lan_discovery: bool = Field(
        ...,
        description=(
            "Defines if the server will listen to LAN discovery requests. Can"
            " be turned off for dedicated servers."
        ),
    )
    config_version: str
    config_public_ip: str = Field(
        ...,
        description=(
            "Explicitly defines the public IP address. Useful if the backend is"
            " connected via a load balancer or reverse proxy. Attention: If"
            " used, the server must use the same port number for tcpPort and"
            " udpPort (e.g. 9231 for both), and respond to an additional"
            " handshake on the UDP port one number higher (e.g. 9232) than its"
            " udpPort, or it will shutdown during startup."
        ),
    )


class ProcessInfo(BaseModel):
    process_is_running: bool
    process_last_start: datetime
    process_last_stop: datetime
    process_id: int


class ServerConfigProcessInfo(ServerConfig, ProcessInfo):
    pass


class ServerConfigCreate(ServerConfig):
    pass


class ServerConfigUpdate(ServerConfig, metaclass=AllOptional):
    pass


class ServerConfigResponse(ServerConfigProcessInfo):
    id: int
    event: EventResponse


class ServerConfigSearchResponse(BaseModel):
    total_count: int
    items: list[ServerConfigResponse]
