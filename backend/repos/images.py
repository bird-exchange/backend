from sqlalchemy.exc import IntegrityError
from backend.db import get_db_session
from backend.models import Image
from backend.errors import ConflictError, NotFoundError


class ImageRepo():
    name = "image"

    def add_image(self, name: str, type: int) -> Image:
        try:
            new_image = Image(name=name, type=type)
            db_session = get_db_session()
            db_session.add(new_image)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return new_image

    def get_all(self) -> list[Image]:
        return Image.query.all()

    def get_by_id(self, uid: int) -> Image:
        image = Image.query.filter(Image.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        return image

    def delete_all(self) -> None:
        db_session = get_db_session()
        entities = Image.query.all()
        for entity in entities:
            local_object = db_session.merge(entity)
            db_session.delete(local_object)
            db_session.commit()

    def delete_by_id(self, uid: int) -> None:
        db_session = get_db_session()
        entity = Image.query.filter(Image.uid == uid).first()
        db_session.delete(entity)
        db_session.commit()

    def update_by_id(self, uid: int, name: str, path_original: str,
                     path_result: str, type: int, was_fitted: int
                     ) -> Image:
        image = Image.query.filter(Image.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        try:
            db_session = get_db_session()
            local_image = db_session.merge(image)
            local_image.name = name
            local_image.path_original = path_original
            local_image.path_result = path_result
            local_image.type = type
            local_image.was_fitted = was_fitted
            db_session.commit()
        except IntegrityError:
            ConflictError(self.name)
        return local_image
