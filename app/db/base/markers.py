from typing import Dict

from app.models.data.project import ProjectFull, Level, Element
from app.models.request.project import MarkerObj
from app.services.deta import get_deta

MARKERS_DB = "markers"


def get_base():
    deta = get_deta()
    db = deta.Base(MARKERS_DB)
    return db


def add_project_full(project_full: ProjectFull):
    db = get_base()
    db.put(project_full.dict())


def get_project_full(project_id: str):
    db = get_base()
    project_obj_list = db.fetch({'project_id': project_id}).items
    return project_obj_list[0] if project_obj_list else None


def get_markers(project_id: str, level: int, element: str):
    project_obj = get_project_full(project_id)
    if project_obj:
        project_full_obj: ProjectFull = ProjectFull(**project_obj)
        _level: Level = project_full_obj.levels[level]
        if _level:
            _element: Element = _level.elements.get(element, None)
            return _element
    return None


def add_markers(project_id: str,
                level: int,
                element: str,
                markers: Dict[str, MarkerObj]):
    db = get_base()
    _element = get_markers(project_id, level, element)
    if _element:
        _current_markers = _element.markers
        # _updated_markers = {**_current_markers, **markers}
        _updated_markers = markers
        _mapped_dict = {k: v.dict() for k, v in _updated_markers.items()}

        project_full_obj = get_project_full(project_id)
        project_key = project_full_obj.get('key', None)
        if project_key:
            updates = {
                f"levels.{level}.elements.{element}.markers": _mapped_dict
            }
            db.update(updates, project_key)
            return "Markers Added Successfully", 200

    return "Some Error Occurred While Adding Markers", 500
