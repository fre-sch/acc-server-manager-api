import os
import pathlib
from datetime import datetime

from acc_server_mgr.models.db import ServerConfig

TMP_PATH = pathlib.Path("")


def start_server(server_config: ServerConfig):
    server_config_file_path = TMP_PATH / "server_config.ini"
    with open(server_config_file_path, "w") as fp:
        fp.write(server_config.config)

    server_config.process_id = os.spawnl(
        os.P_NOWAIT, "server", "args", server_config_file_path
    )
    server_config.is_running = True
    server_config.last_start = datetime.now()
    return server_config


def stop_server(server_config):
    os.spawnl(os.P_NOWAIT, "taskkill", "/F", "/PID", str(server_config.process_id))
    server_config.last_stop = datetime.now()
    server_config.is_running = False
    server_config.process_id = 0
    return server_config
