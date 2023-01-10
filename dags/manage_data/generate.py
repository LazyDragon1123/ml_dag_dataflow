import json
import random

from sqlalchemy import create_engine

from manage_data._config import db_string


def _rand_payload():
    payload = {}
    if random.randint(0, 10) > 5:
        payload = {
            "value": f"{random.randint(0, 1000)}",
            "score": round(random.random(), 2),
            "ocr_score": round(random.random(), 2),
            "bounding_box": [round(random.random(), 2) for i in range(4)],
        }
    return payload


def _generate_input():
    choices = [
        _rand_payload(),
        [_rand_payload() for i in range(0, 9)],
    ]
    payloads = {"business_id": random.randint(0, 9)}
    fields = ["total", "line_items"]
    for f in fields:
        payloads[f] = choices[random.randint(0, 9) % len(fields)]
    return json.dumps(payloads)


def create_receipt():
    db = create_engine(db_string)
    db.execute("INSERT INTO documents (ml_response) " + "VALUES ('" + _generate_input() + "');")
