from project import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    avg_score = db.Column(db.Float(), nullable=False, default=0.0)
    creator = db.Column(db.String(128), nullable=False)

    def __init__(self, type, number, creator):
        self.type = type
        self.id = number
        self.creator = creator

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'average score': self.avg_score,
            'creator': self.creator
        }
