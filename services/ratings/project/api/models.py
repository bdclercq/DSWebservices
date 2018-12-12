from sqlalchemy.sql import func

from project import db


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stop_name = db.Column(db.String(128), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, stop_name, score, description):
        self.stop_name = stop_name
        self.score = score
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'stop': self.stop_name,
            'score': self.score,
            'description': self.description
        }
