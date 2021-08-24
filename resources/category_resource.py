from typing import List

from repository.database import Database
from repository.category_repository import CategoryRepository

from model.category_model import Category
from model.category_model import Category

from core import handling_error as error


class CategoryResource():

    def __init__(self) -> None:
        self.repository = CategoryRepository(Database())

    def get_category_by_id(self, id: int) -> Category:
        category = self.repository.get_category_by_id(id)
        if category is None:
            raise error.http_404_object_not_found("Category not found!", "category_not_found")
        return category

    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all_categories()

