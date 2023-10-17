"""Module to configure Flask app"""
from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import routes # This line is needed, even though Pylint (and perhaps others) don't agree.