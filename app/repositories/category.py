from app.models.category import CategoryORM
from sqlalchemy import select
from sqlalchemy.orm import Session

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def create_category(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        self.db.flush()
        return new_category

    def delete_category(self, category: CategoryORM) -> None:
        self.db.delete(category)
    