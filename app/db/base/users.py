from app.models.data.users import UserShort, UserFull
from app.services.deta import get_deta

USER_DB = "users"
deta = get_deta()
db = deta.Base(USER_DB)


def get_users():
    _users = db.fetch().items
    return [UserShort(**_user) for _user in _users]


def add_user(user: UserShort):
    _full_user: UserFull = UserFull(**user.dict())
    return db.put(_full_user.dict())


def get_user(user_id: str):
    user_obj_list = db.fetch({'id': user_id}).items
    return user_obj_list[0] if user_obj_list else None


def update_user(user: UserFull):
    _user_key = user.dict().get('key', None)
    if _user_key:
        return db.put(user.dict(), _user_key)
    return "Provided User Not Found", 404


def remove_user(user_key: str):
    return db.delete(user_key)


def add_project(user_id: str, project_id: str):
    _user_dict = get_user(user_id)
    if _user_dict:
        _user: UserFull = UserFull(**_user_dict)
        _user_key = _user.dict().get('key', None)
        _projects = _user.projects
        _projects = list(set(_projects + [project_id]))
        if _user_key:
            updates = {
                f"projects": _projects
            }
            db.update(updates, _user_key)
            return "Project Added Successfully", 200
    else:
        raise KeyError("UserId Is Not Found")


def remove_project(user_id: str, project_id: str):
    _user: UserFull = UserFull(**get_user(user_id))
    if _user:
        _user_key = _user.dict().get('key', None)
        _projects = _user.projects
        if project_id in _projects:
            _projects = [pr for pr in _projects if pr != project_id]
            if _user_key:
                updates = {
                    f"projects": _projects
                }
                db.update(updates, _user_key)
                return "Project Removed Successfully", 200
