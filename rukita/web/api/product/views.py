from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from rukita.db.dao.product_dao import ProductDAO
from rukita.db.exceptions import ProductNotFoundException
from rukita.db.models.product_model import ProductModel
from rukita.web.api.product.schema import (
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema
)

router = APIRouter()


@router.get("/products", response_model=List[ProductSchema])
async def products(
    limit: int = 10,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
) -> List[ProductModel]:
    """
    Retrieve all product objects from the database.

    :param limit: limit of product objects, defaults to 10.
    :param offset: offset of product objects, defaults to 0.
    :param product_dao: DAO for product models.
    :return: list of product objects from database.
    """
    return await product_dao.get_all_products(limit=limit, offset=offset)


@router.post("/products", response_model=None)
async def create_product(
    product_dto: ProductCreateSchema,
    product_dao: ProductDAO = Depends(),
) -> None:
    """
    Creates product model in the database.

    :param product_dto: new product model item.
    :param product_dao: DAO for product models.
    """
    await product_dao.create_product_model(**product_dto.dict())
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/products/{product_id}", response_model=ProductSchema)
async def retrieve_product(
    product_id: int,
    product_dao: ProductDAO = Depends(),
) -> Optional[ProductModel]:
    """
    Retrieve specific product from the database.

    :param product_id: id of product instance.
    :param product_dao: DAO for product models.
    :return: product models.
    """
    product = await product_dao.get_by_id(product_id=product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_dto: ProductUpdateSchema,
    product_dao: ProductDAO = Depends(),
) -> Optional[ProductModel]:
    """
    Retrieve specific product from the database.

    :param product_id: id of product instance.
    :param product_dao: DAO for product models.
    :return: product models.
    """
    try:
        return await product_dao.update_product(
            product_id=product_id,
            title=product_dto.title,
            description=product_dto.description,
            stocks=product_dto.stocks,
        )
    except ProductNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
