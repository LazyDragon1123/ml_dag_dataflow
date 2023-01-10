import json

from sqlalchemy import create_engine

from manage_data._config import db_string


def _get_last_row(db):
    query = (
        ""
        + "SELECT ml_response "
        + "FROM documents "
        + "WHERE document_id >= (SELECT max(document_id) FROM documents)"
        + "LIMIT 1"
    )
    result_set = db.execute(query)
    for r in result_set:
        return r[0]


def _is_empty(parsed):
    if not bool(parsed):
        return True
    elif isinstance(parsed, list) and all([not bool(p) for p in parsed]):
        return True


def extract():
    db = create_engine(db_string)
    parsed = json.loads(_get_last_row(db))
    if _is_empty(parsed["total"]):
        return None
    else:
        if isinstance(parsed["total"], dict):
            return {
                "business_id": parsed["business_id"],
                "sum_total": parsed["total"]["value"],
                "sum_ai_score": parsed["total"]["score"],
                "sum_ocr_score": parsed["total"]["ocr_score"],
                "num_data": 1,
                "bbox": json.dumps(parsed["total"]["bounding_box"]),
            }
        elif isinstance(parsed["total"], list):
            sum_total = sum_ai_score = sum_ocr_score = 0
            bbox = ""
            for each in parsed["total"]:
                if bool(each):
                    sum_total += float(each["value"])
                    sum_ai_score += each["score"]
                    sum_ocr_score += each["ocr_score"]
                    bbox += json.dumps(each["bounding_box"]) + ", "
            return {
                "business_id": parsed["business_id"],
                "sum_total": sum_total,
                "sum_ai_score": sum_ai_score,
                "sum_ocr_score": sum_ocr_score,
                "num_data": len(parsed["total"]),
                "bbox": bbox[:-2],
            }
        else:
            return None
