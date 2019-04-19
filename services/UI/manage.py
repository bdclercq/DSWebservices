import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import UI  # new
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'a80d6af91407478c91c8288afd85452f',
}

if __name__ == '__main__':
    cli()
