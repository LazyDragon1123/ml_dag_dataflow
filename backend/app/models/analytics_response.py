from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total: float
    average_ai_score: float
    average_ocr_score: float
    num_valid_receipts: int
    business_id: int
    bbox: str
