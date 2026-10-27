from app.schemas.category import CategorySchema, CategoryCreateSchema , CategoryUpdateSchema
from app.repositories.category import CategoryRepository
from sqlalchemy.orm import Session



class CategoryNotFound(Exception):
    pass


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all_categories()
        return [CategorySchema.model_validate(c) for c in categories_orm]

    def update_category(self, category_id, category_update: CategoryUpdateSchema):
        category_for_update = self.category_repository.get_by_id(category_id=category_id)
        if category_for_update is None:
            raise CategoryNotFound('ne naidena')

        data = category_update.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(category_for_update, field, value)

        self.db.commit()
        self.db.refresh(category_for_update)
        return CategorySchema.model_validate(category_for_update)

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category_orm_cr = self.category_repository.create_category(name=category_create.name)
        self.db.commit()
        self.db.refresh(category_orm_cr)
        return CategorySchema.model_validate(category_orm_cr)

    def delete_category(self, category_id):
        category_for_delete = self.category_repository.get_by_id(category_id=category_id)
        if category_for_delete is None:
            raise CategoryNotFound('ne naidena')
        self.category_repository.delete_category(category_for_delete)
        self.db.commit()