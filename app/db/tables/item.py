from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    """Represent the grocery store items"""
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = None
