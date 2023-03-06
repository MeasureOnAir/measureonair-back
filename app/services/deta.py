from deta import Deta
from app.conf import config

# Get Application Settings
settings = config.get_settings()


def get_deta():
    deta = Deta(settings.deta_settings.deta_project_key)
    return deta
