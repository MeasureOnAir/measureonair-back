from app.modals.data.project import ProjectMeta
from app.services.deta import get_deta

META_DB = "meta"


def get_base():
    deta = get_deta()
    db = deta.Base(META_DB)
    return db


def add_project_meta(project_meta: ProjectMeta):
    db = get_base()
    return db.put(project_meta.dict())


def get_project_all():
    db = get_base()
    return db.fetch().items
