import os, sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(128), nullable=False)
	email = db.Column(db.String(128), nullable=False)
	password = db.Column(db.String(50), nullable=False)
	active = db.Column(db.Boolean(), default=True, nullable=False)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password


#print(app.config, file=sys.stderr)

@app.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong'
	})
