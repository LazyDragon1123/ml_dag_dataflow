import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine

from app._config import db_string
from app.models.analytics_response import AnalyticsResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{business_id}")
async def get_analytics_by_id(business_id: str) -> Optional[AnalyticsResponse]:
    try:
        db = create_engine(db_string)
        query = (
            ""
            + "SELECT total, ai_score, ocr_score, num_data, bbox "
            + "FROM parsed_total "
            + f"WHERE business_id = {business_id};"
        )
        rs = db.execute(query)
        for r in rs:
            return AnalyticsResponse(
                total=r["total"],
                average_ai_score=r["ai_score"],
                average_ocr_score=r["ocr_score"],
                num_valid_receipts=r["num_data"],
                business_id=int(business_id),
                bbox=r["bbox"],
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.delete("/{business_id}")
async def delete_analytics_by_id(business_id: str) -> None:
    try:
        db = create_engine(db_string)
        query = "" + "DELETE FROM parsed_total " + f"WHERE business_id = {business_id};"
        db.execute(query)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
