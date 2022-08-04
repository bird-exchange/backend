from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Bird


class BirdRepo():
    name = "bird"

    def add_bird(self, uid: int, name: str, type: int, was_fitted: int
                 ) -> Bird:

        try:
            new_bird = Bird(
                name=name,
                type=type,
                was_fitted=was_fitted
            )
            db_session.add(new_bird)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return new_bird

    def get_all(self) -> list[Bird]:
        return Bird.query.all()

    def get_all_sparrow(self) -> list[Bird]:
        return Bird.query.filter(Bird.type == 2).all()

    def get_all_tit(self) -> list[Bird]:
        return Bird.query.filter(Bird.type == 1).all()

    def get_by_id(self, uid: int) -> Bird:
        bird = Bird.query.filter(Bird.uid == uid).first()
        if not bird:
            raise NotFoundError(self.name)
        return bird

    def get_not_recognized(self) -> Bird:
        bird = Bird.query.filter(Bird.was_fitted == 0).first()
        if not bird:
            raise NotFoundError(self.name)
        return bird

    def delete_all(self) -> None:
        birds = Bird.query.all()
        for bird in birds:
            db_session.delete(bird)
            db_session.commit()

    def delete_by_id(self, uid: int) -> None:
        bird = Bird.query.filter(Bird.uid == uid).first()
        if not bird:
            raise NotFoundError(self.name)
        db_session.delete(bird)
        db_session.commit()

    def update_by_id(self, uid: int, name: str, type: int, was_fitted: int
                     ) -> Bird:
        bird = Bird.query.filter(Bird.uid == uid).first()
        if not bird:
            raise NotFoundError(self.name)
        try:
            bird.name = name
            bird.type = type
            bird.was_fitted = was_fitted
            db_session.commit()
        except IntegrityError:
            ConflictError(self.name)
        return bird
