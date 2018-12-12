from sqlalchemy.sql import func

from project import db


class Stop(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stop_name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    avg_score = db.Column(db.Float(), nullable=False, default=0.0)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, stop_name, location):
        self.stop_name = stop_name
        self.location = location

    def to_json(self):
        return {
            'id': self.id,
            'stop': self.stop_name,
            'location': self.location,
            'average score': self.avg_score
        }
