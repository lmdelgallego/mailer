from flask import Blueprint, render_template, request, jsonify
from app.db import get_db

bp = Blueprint("mail", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def index():
    db, cursor = get_db()

    cursor.execute("SELECT * FROM email")
    mails = cursor.fetchall()

    return render_template("index.html", mails=mails)
