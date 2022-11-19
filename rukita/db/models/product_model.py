from datetime import datetime

from rukita.db.base import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text


class ProductModel(Base):
    """Model Product"""

    __tablename__ = "product_model"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(length=200))  # noqa: WPS432
    description = Column(Text())
    stocks = Column(Integer())
    created = Column(DateTime(), default=datetime.utcnow)
    updated = Column(
        DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
