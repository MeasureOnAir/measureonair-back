from typing import List, Union, Dict
from pydantic import BaseModel, EmailStr, AnyUrl


class UserShort(BaseModel):
    id: str
    name: str
    email: EmailStr


class UserFull(BaseModel):
    key: Union[str, None]
    id: str
    name: str
    email: EmailStr
    projects: List[str] = []
    profile_picture: AnyUrl = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
    cover_photo: AnyUrl = 'https://i.pinimg.com/originals/83/f2/8e/83f28e151f4a0b99a216abb8e0d72284.jpg'
