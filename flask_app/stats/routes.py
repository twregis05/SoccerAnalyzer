from flask import Flask, Blueprint

stats = Blueprint("stats", __name__)


@stats.route('/')
def hello():
    return "Hello Soham"

