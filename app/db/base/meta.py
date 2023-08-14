from app.db.base.users import get_user
from app.models.data.project import ProjectMeta
from app.services.deta import get_deta

META_DB = "meta"


def get_base():
    deta = get_deta()
    db = deta.Base(META_DB)
    return db


def add_project_meta(project_meta: ProjectMeta):
    db = get_base()
    return db.put(project_meta.dict())


def get_project_all(user_id: str):
    db = get_base()
    _user = get_user(user_id)
    if _user:
        _user_projects = _user['projects']
        _projects = db.fetch().items
        return [project for project in _projects if project['id'] in _user_projects]
    else:
        return False

