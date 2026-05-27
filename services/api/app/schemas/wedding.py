from typing import Optional

from pydantic import BaseModel, Field


class VendorCategoryRead(BaseModel):
    id: str
    label: str
    description: str
    icon: str
    bodas_path: str
    vendor_count: int


class VendorCard(BaseModel):
    id: str
    name: str
    category: str
    category_label: str
    city: str
    region: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_from: Optional[float] = None
    price_label: Optional[str] = None
    short_description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    capacity_min: Optional[int] = None
    capacity_max: Optional[int] = None
    featured: bool = False
    promotion: Optional[str] = None
    availability_hint: Optional[str] = None
    image_url: Optional[str] = None


class VendorSearchResponse(BaseModel):
    total: int
    category: Optional[str] = None
    city: Optional[str] = None
    query: Optional[str] = None
    results: list[VendorCard]
