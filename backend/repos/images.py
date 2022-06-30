from sqlalchemy.exc import IntegrityError
from backend.db import get_db_session
from backend.models import Image
from backend.errors import ConflictError


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
