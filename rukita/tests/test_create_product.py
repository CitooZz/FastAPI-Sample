from http import HTTPStatus
from typing import Optional

import pytest

from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_product_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
) -> None:
    """
    Checks create product /api/products endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    """
    url = fastapi_app.url_path_for("create_product")
    response = await client.post(url, json=create_product_payload)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.parametrize(
    "field, value",
    [
        ("title", None),
        ("title", ""),
        ("description", None),
        ("description", ""),
        ("stocks", None),
        ("stocks", -1),
    ],
)
@pytest.mark.anyio
async def test_validate_payload(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
    field: str,
    value: Optional[str],
) -> None:
    """
    Checks create product /api/products endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    """
    create_product_payload[field] = value

    url = fastapi_app.url_path_for("create_product")
    response = await client.post(url, json=create_product_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
