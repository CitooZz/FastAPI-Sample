from http import HTTPStatus

import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from .test_create_product import test_create_product_success


@pytest.mark.anyio
async def test_retrieve_product_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
) -> None:
    """
    Checks retrieve product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    """
    await test_create_product_success(
        client,
        fastapi_app,
        create_product_payload,
    )

    url = fastapi_app.url_path_for("retrieve_product", product_id=4)
    response = await client.get(url)
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    for field, value in create_product_payload.items():
        assert response_data[field] == value


@pytest.mark.anyio
async def test_retrieve_product_not_found(
    client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    """
    Checks retrieve product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("retrieve_product", product_id=200)
    response = await client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
