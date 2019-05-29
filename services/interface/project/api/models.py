from project import db


class Interface(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initialized = False

    def __init__(self):
        self.initialized = True
