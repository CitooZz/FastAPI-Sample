from http import HTTPStatus
from typing import Optional

import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from .test_create_product import test_create_product_success


@pytest.mark.anyio
async def test_update_product_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
) -> None:
    """
    Checks update product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param product: existing product.
    :param create_product_payload: create product parameters.
    """
    await test_create_product_success(
        client,
        fastapi_app,
        create_product_payload,
    )

    create_product_payload["title"] = "Edited"
    url = fastapi_app.url_path_for("update_product", product_id=5)
    response = await client.put(url, json=create_product_payload)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == create_product_payload["title"]


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
    Checks update product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    :param field: field parameter from decorator.
    :param value: value parameter from decorator.
    """
    create_product_payload[field] = value

    url = fastapi_app.url_path_for("update_product", product_id=1)
    response = await client.put(url, json=create_product_payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
