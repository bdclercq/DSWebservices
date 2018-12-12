import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import Stop  # new
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

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
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/v1/beta/haltes", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data = json.loads(data)
    for i in range(len(data["haltes"])):
        try:
            name = data["haltes"][i]["omschrijving"]
            location = data["haltes"][i]["omschrijvingGemeente"]
            # print(i, len(data["haltes"]))
            db.session.add(Stop(stop_name=name, location=location))
            db.session.commit()
        except:
            pass
    # db.session.add(Stop(stop_name='Burgemeester Nolf', location="Merksem"))
    # db.session.commit()


if __name__ == '__main__':
    cli()
