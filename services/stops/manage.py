import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import Stop  # new
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import requests

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'a80d6af91407478c91c8288afd85452f',
}


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seeds the database."""
    print("Getting data from API ...")
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/v1/beta/haltes", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    print("Got data, start processing ...")
    data = json.loads(data)
    failed_count = 0
    total_stops = len(data['haltes'])
    for stop in data['haltes']:
        try:
            name = stop['omschrijving']
            number = stop['haltenummer']
            location = stop['omschrijvingGemeente']
            prov = int(stop['entiteitnummer'])
            lat = float(stop['geoCoordinaat']['latitude'])
            lon = float(stop['geoCoordinaat']['longitude'])
            # print(i, len(data["haltes"]))
            print(name, ', ', number, ', ', location, ', ', prov, ', ', lat, ', ', lon)
            db.session.add(Stop(nr=number, stop_name=name, location=location, lat=lat, lon=lon, prov=prov))
            db.session.commit()
        except KeyError as ke:
            print("Cannot add stop: ", str(ke))
            failed_count += 1
            pass
    print("From ", total_stops, ", ", total_stops-failed_count, " were added")

    # db.session.add(Stop(stop_name='Burgemeester Nolf', location="Merksem"))
    # db.session.commit()


if __name__ == '__main__':
    cli()
