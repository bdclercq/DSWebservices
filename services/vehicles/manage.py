import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import Vehicle  # new

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command()
# def seed_db():
#     """Seeds the database."""
#     db.session.add(Vehicle(type='bus', number=33))
#     db.session.commit()


if __name__ == '__main__':
    cli()
