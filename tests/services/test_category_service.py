from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound, CategoryService


def test_list_tasks_return_pydantic_model(
    category_service: CategoryService,
    category_repository_mock: Mock,
):
    category_repository_mock.get_all_categories.return_value = [
        CategoryORM(id="1", name="test_category"),
        CategoryORM(id="2", name="test_category2"),
    ]

    result = category_service.list_categories()

    assert result == [
        CategorySchema(id="1", name="test_category"),
        CategorySchema(id="2", name="test_category2"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
):
    category_repository_mock.create_category.return_value = CategoryORM(
        id="1", name="test_category"
    )
    result = category_service.create_category(
        CategoryCreateSchema(name="test_category")
    )

    category_repository_mock.create_category.assert_called_once_with(
        name="test_category"
    )
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": "1",
        "name": "test_category",
    }


def test_update_category_updates_name(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
):
    category = CategoryORM(id="1", name="test_category")
    payload = CategoryUpdateSchema(name="test_category")

    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category(category_id="1", category_update=payload)

    category_repository_mock.get_by_id.assert_called_once_with(category_id="1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "1",
        "name": "test_category",
    }


def test_update_category_returns_none_if_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
):
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.update_category(
            category_id="1", category_update=CategoryUpdateSchema(name="test_category")
        )

    db_mock.commit.assert_not_called()
