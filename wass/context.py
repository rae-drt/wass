from dataclasses import dataclass
from configparser import ConfigParser

config_ini = ConfigParser()
config_ini.read("config.ini")

@dataclass
class Context:
    version = config_ini.get("main", "VERSION")
    annotation_limit = config_ini.getint("wass", "ANNOTATION_LIMIT")
    annotation_server = config_ini.get("wass", "ANNOTATION_SERVER")
    cosine_distance = config_ini.getfloat("wass", "COSINE_DISTANCE")
    server_ip = config_ini.get("wass", "SERVER_IP") 
    server_port = config_ini.getint("wass", "SERVER_PORT")
    debug = config_ini.getboolean("wass", "DEBUG")
    cors = config_ini.getboolean("wass", "CORS")
    db = config_ini.get("wass", "DB")

