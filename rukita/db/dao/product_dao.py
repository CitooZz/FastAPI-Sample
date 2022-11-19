from typing import List, Optional

from fastapi import Depends
from rukita.db.dependencies import get_db_session
from rukita.db.exceptions import ProductNotFoundException
from rukita.db.models.product_model import ProductModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProductDAO:
    """Class for accessing product table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_product_model(
        self,
        title: str,
        description: str,
        stocks: int,
    ) -> None:
        """
        Add single dummy to session.

        :param title: title of a product.
        :param description: description of a product.
        :param stocks: stocks of a product.
        """
        self.session.add(
            ProductModel(title=title, description=description, stocks=stocks),
        )

    async def get_all_products(self, limit: int, offset: int) -> List[ProductModel]:
        """
        Get all product models with limit/offset pagination.

        :param limit: limit of products.
        :param offset: offset of products.
        :return: stream of products.
        """
        raw_products = await self.session.execute(
            select(ProductModel).limit(limit).offset(offset),
        )

        return raw_products.scalars().fetchall()

    async def get_by_id(
        self,
        product_id: int,
    ) -> Optional[ProductModel]:
        """
        Get specific product model.

        :param id: id of dummy instance.
        :return: product model.
        """
        return await self.session.get(ProductModel, product_id)

    async def update_product(
        self,
        product_id: int,
        title: str,
        description: str,
        stocks: int,
    ) -> ProductModel:
        """
        Update specific product model.

        :param title: title of a product.
        :param description: description of a product.
        :param stocks: stocks of a product.
        :return: product model.
        """
        product = await self.session.get(ProductModel, product_id)

        if product is None:
            raise ProductNotFoundException()

        product.title = title
        product.description = description
        product.stocks = stocks
        await self.session.commit()
        await self.session.refresh(product)
        return product
