from datetime import datetime

from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """
    Schema for product models.
    """

    id: int
    title: str
    description: str
    stocks: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class ProductCreateSchema(BaseModel):
    """
    Schema for create product.
    """

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    stocks: int = Field(gt=0)


class ProductUpdateSchema(ProductCreateSchema):
    """
    Schema for update product.
    """

    pass
