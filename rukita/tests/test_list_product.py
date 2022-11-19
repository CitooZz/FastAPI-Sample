from http import HTTPStatus

import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from .test_create_product import test_create_product_success


@pytest.mark.anyio
async def test_list_product_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
) -> None:
    """
    Checks list product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    """
    await test_create_product_success(
        client,
        fastapi_app,
        create_product_payload,
    )

    url = fastapi_app.url_path_for("products")
    response = await client.get(url)
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == 1
    for field, value in create_product_payload.items():
        assert response_data[0][field] == value


@pytest.mark.parametrize(
    "limit, offset, expected_count",
    [
        (10, 0, 1),
        (10, 3, 0),
    ],
)
@pytest.mark.anyio
async def test_list_product_pagination(
    client: AsyncClient,
    fastapi_app: FastAPI,
    create_product_payload: dict,
    limit: int,
    offset: int,
    expected_count: int,
) -> None:
    """
    Checks list product endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param create_product_payload: create product parameters.
    :param limit: limit parameter from decorator.
    :param offset: offset parameter from decorator.
    :param expected_count: expected_count parameter from decorator.
    """

    await test_create_product_success(
        client,
        fastapi_app,
        create_product_payload,
    )
    url = fastapi_app.url_path_for("products")
    response = await client.get(f"{url}?limit={limit}&offset={offset}")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == expected_count
