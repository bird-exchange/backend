from backend.models import Image


class ImageRepo():
    name = "image"

    def get_all(self) -> list[Image]:
        return Image.query.all()
