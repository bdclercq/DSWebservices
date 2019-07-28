from sqlalchemy.sql import func

from project import db


class Stop(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.Integer, nullable=False)
    stop_name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    lat = db.Column(db.Float(), nullable=False)
    lon = db.Column(db.Float(), nullable=False)
    avg_score = db.Column(db.Float(), nullable=False, default=0.0)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, nr, stop_name, location, lat, lon, prov):
        self.id = nr
        self.stop_name = stop_name
        self.location = location
        self.lat = lat
        self.lon = lon
        self.province = prov

    def to_json(self):
        return {
            'id': self.id,
            'stop': self.stop_name,
            'location': self.location,
            'lat': self.lat,
            'lon': self.lon,
            'prov': self.province,
            'average_score': self.avg_score
        }
