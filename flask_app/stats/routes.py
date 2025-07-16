from flask import Flask, Blueprint, redirect, url_for, render_template

stats = Blueprint("stats", __name__)


@stats.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

