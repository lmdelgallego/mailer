from flask import Blueprint, render_template, request, jsonify
from app.db import get_db

bp = Blueprint("mail", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def index():
    db, cursor = get_db()

    cursor.execute("SELECT * FROM email")
    mails = cursor.fetchall()

    return render_template("index.html", mails=mails)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        db, cursor = get_db()

        email = request.form["email"]
        subject = request.form["subject"]
        content = request.form["content"]

        cursor.execute(
            "INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)",
            (email, subject, content),
        )
        db.commit()

        return jsonify({"success": True})

    return render_template("mails/create.html")
