from io import BytesIO
from typing import Dict

from openpyxl import Workbook
from starlette.responses import StreamingResponse

from app.db.base import markers
from app.models.data.marker import Marker
from app.models.data.project import ProjectFull, Level
from app.models.request.project import MarkerObj

ELEMENTS = {'EL001': "floor", 'EL002': "wall", 'EL003': "door", 'EL004': "window", 'EL005': "paint", 'EL006': "roof"}


def get_spread_sheet(project_id: str, level: int, element_id: str):
    project_full_obj: ProjectFull = ProjectFull(**markers.get_project_full(project_id))
    _level: Level = project_full_obj.levels[level]
    _markers = _level.elements[element_id].markers
    if _markers:
        workbook = create_excel_sheet(_markers, project_full_obj.project_meta.name, level, ELEMENTS.get(element_id))

        file_stream = BytesIO()
        workbook.save(file_stream)
        file_stream.seek(0)

        return StreamingResponse(file_stream,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        return 'Error: Object Not Found!', 404


def create_excel_sheet(record_data: Dict[str, MarkerObj], project_name, level, element_name):
    workbook = Workbook()
    sheet = workbook.active
    # Header
    sheet["A1"] = "Project Name:"
    sheet["B1"] = project_name
    sheet["A2"] = "Level No:"
    sheet["B2"] = level
    sheet["A3"] = "Element Name:"
    sheet["B3"] = element_name

    # Table Headers
    sheet["A5"] = "Ref ID"
    sheet["B5"] = "Length"
    sheet["C5"] = "Width"
    sheet["D5"] = "Height"
    sheet["E5"] = "Volume"
    sheet["F5"] = "Times"
    sheet["G5"] = "Total"
    sheet["H5"] = "Unit"
    sheet["I5"] = "Remarks"

    # Add Marker Data
    for idx, (key, value) in enumerate(record_data.items()):
        data: Marker = value.data
        sheet[f"A{idx + 6}"] = key
        sheet[f"B{idx + 6}"] = data.length
        sheet[f"C{idx + 6}"] = data.width
        sheet[f"D{idx + 6}"] = data.height
        sheet[f"E{idx + 6}"] = data.length * data.width * data.height
        sheet[f"F{idx + 6}"] = data.times
        sheet[f"G{idx + 6}"] = data.length * data.width * data.height * data.times
        sheet[f"H{idx + 6}"] = data.unit
        sheet[f"I{idx + 6}"] = data.remarks

    return workbook
