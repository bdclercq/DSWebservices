from sqlalchemy.sql import func

from project import db


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_for = db.Column(db.String(128), nullable=False)
    score = db.Column(db.Float(), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    rating_type = db.Column(db.Integer, default=0, nullable=False)     # 0 for vehicle, 1 for stop
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, rating_for, score, description, rating_type):
        self.rating_for = rating_for
        self.score = score
        self.description = description
        self.rating_type = rating_type

    def to_json(self):
        return {
            'id': self.id,
            'rating_for': self.rating_for,
            'score': self.score,
            'description': self.description,
            'rating_type': self.rating_for
        }
