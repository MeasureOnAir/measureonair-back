from pydantic import BaseSettings, BaseModel
from functools import lru_cache
import configparser

deta_config = configparser.ConfigParser()
deta_config.read('app/conf/deta.ini')


class Settings(BaseSettings):
    app_name: str = "MOA-Backend"
    server_env: str = "LOCAL"
    serve_ip: str = "0.0.0.0"
    serve_port: int = 8000

    # class Config:
    #     env_file = ".env"


class DetaSettings(BaseModel):
    deta_username: str = "neura"
    deta_password: str = "zaq123WSX"
    # deta_project_key: str = "d0w1tcdj_HfBi7YEfvWGWcFiACfpYYtgbZaKa9kzV"
    deta_project_key: str = "c0GW6XkWPn76_vGSWE5xwk6gc8wrfVdPMxgNXtihYqQex"


class AppSettings(BaseModel):
    env_settings: Settings
    deta_settings: DetaSettings


@lru_cache()
def get_settings():
    settings = AppSettings(
        env_settings=Settings(),
        deta_settings=DetaSettings.parse_obj(deta_config[Settings().server_env]),
    )
    # settings = AppSettings(**docdb_config[Settings().server_env])
    return settings

# Key Name:            ubt28
# Key Description:     Project Key: ubt28
# Project Key:         d0w1tcdj_HfBi7YEfvWGWcFiACfpYYtgbZaKa9kzV


# {
# 	"name": "moa-backend",
# 	"id": "871d7422-4b19-4c66-99d4-d464676db9af",
# 	"project": "d0w1tcdj",
# 	"runtime": "python3.9",
# 	"endpoint": "https://qsmigu.deta.dev",
# 	"region": "ap-south-1",
# 	"visor": "disabled",
# 	"http_auth": "disabled"
# }
