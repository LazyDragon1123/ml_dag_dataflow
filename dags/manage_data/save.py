from manage_data._config import db_string
from sqlalchemy import create_engine


def _exists_id(db, business_id):
    query = "" + "SELECT " + "EXISTS( " + "SELECT 1 FROM parsed_total " + f"WHERE business_id = {business_id});"
    rs = db.execute(query)
    for r in rs:
        return r[0]


def _get_by_id(db, business_id):
    query = (
        ""
        + "SELECT total, ai_score, ocr_score, num_data, bbox "
        + "FROM parsed_total "
        + f"WHERE business_id = {business_id};"
    )
    rs = db.execute(query)
    for r in rs:
        return r


def _update_by_id(db, data, business_id):
    query = (
        ""
        + "UPDATE parsed_total "
        + f'SET total = {data["total"]}, ai_score = {data["ai_score"]}, ocr_score = {data["ocr_score"]}, num_data = {data["num_data"]}, bbox = '
        + "'"
        + f'{data["bbox"]}'
        + "' "
        f"WHERE business_id = {business_id};"
    )
    db.execute(query)


def _insert(db, data, business_id):
    query = (
        "INSERT INTO parsed_total (business_id, num_data, total, ai_score, ocr_score, bbox) "
        + f'VALUES ({business_id}, {data["num_data"]}, {data["total"]}, {data["ai_score"]}, {data["ocr_score"]}, '
        + "'"
        + f'{data["bbox"]}'
        + "');"
    )
    db.execute(query)


def _calculate_score(record, new_data):
    if record is None:
        num_data = new_data["num_data"]
        total = new_data["sum_total"]
        ocr_score = new_data["sum_ocr_score"] / num_data
        ai_score = new_data["sum_ai_score"] / num_data
        bbox = new_data["bbox"]
    else:
        num_data = new_data["num_data"] + record["num_data"]
        total = new_data["sum_total"] + float(record["total"])
        ocr_score = (new_data["sum_ocr_score"] + record["ocr_score"] * record["num_data"]) / num_data
        ai_score = (new_data["sum_ai_score"] + record["ai_score"] * record["num_data"]) / num_data
        bbox = new_data["bbox"] + ", " + record["bbox"]
    return {"total": total, "ai_score": ai_score, "ocr_score": ocr_score, "num_data": num_data, "bbox": bbox}


def push_total(new_data):
    business_id = new_data["business_id"]
    db = create_engine(db_string)
    if _exists_id(db, business_id):
        record = _get_by_id(db, business_id)
        updated_data = _calculate_score(record, new_data)
        _update_by_id(db, updated_data, business_id)
    else:
        updated_data = _calculate_score(None, new_data)
        _insert(db, updated_data, business_id)
