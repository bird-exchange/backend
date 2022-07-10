from sqlalchemy.exc import IntegrityError
from backend.db import db_session
from backend.models import Image
from backend.errors import ConflictError, NotFoundError


class ImageRepo():
    name = "image"

    def add_image(self, uid: int, name: str, type: int, was_fitted: int
                  ) -> Image:

        try:
            new_image = Image(
                name=name,
                type=type,
                was_fitted=was_fitted
            )
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
        images = Image.query.all()
        for image in images:
            db_session.delete(image)
            db_session.commit()

    def delete_by_id(self, uid: int) -> None:
        image = Image.query.filter(Image.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        db_session.delete(image)
        db_session.commit()

    def update_by_id(self, uid: int, name: str, type: int, was_fitted: int
                     ) -> Image:
        image = Image.query.filter(Image.uid == uid).first()
        if not image:
            raise NotFoundError(self.name)
        try:
            image.name = name
            image.type = type
            image.was_fitted = was_fitted
            db_session.commit()
        except IntegrityError:
            ConflictError(self.name)
        return image
