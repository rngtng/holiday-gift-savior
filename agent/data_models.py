"""Data models for the Holiday Gift Savior system."""

from typing import List
from pydantic import BaseModel, Field


class RecipientProfile(BaseModel):
    """Long-term memory profile for a gift recipient."""

    recipient_name: str
    persistent_interests: List[str] = Field(default_factory=list)
    past_successful_gifts: List[str] = Field(default_factory=list)
    disliked_categories: List[str] = Field(default_factory=list)


class GiftIdea(BaseModel):
    """A gift recommendation from the research agents."""

    recipient: str
    gift_title: str
    description: str
    estimated_price: float
    product_link: str
    currency: str = "USD"
    budget_check_status: str = "Pending"