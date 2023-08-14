from io import BytesIO

from starlette.responses import StreamingResponse

from app.services.deta import get_deta

DB_NAME = "images"


def get_drive(path):
    deta = get_deta()
    drive = deta.Drive(path)
    return drive


def get_image(project_id, filename):
    drive = get_drive(project_id)
    file_stream = drive.get(filename)
    file_bytes = file_stream.read()
    return StreamingResponse(BytesIO(file_bytes),
                             media_type=f"image/{filename.split('.')[-1]}")
