from project import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    avg_score = db.Column(db.Float(), nullable=False, default=0.0)
    creator = db.Column(db.String(128), nullable=False)

    def __init__(self, type, number):
        self.type = type
        self.number = number

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'number': self.number,
            'average score': self.avg_score
        }
