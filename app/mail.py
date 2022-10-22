from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
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
        errors = []

        email = request.form["email"]
        subject = request.form["subject"]
        content = request.form["content"]

        if not email:
            errors.append("Email is required.")
        if not subject:
            errors.append("Subject is required.")
        if not content:
            errors.append("Content is required.")

        if len(errors) == 0:
            cursor.execute(
                "INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)",
                (email, subject, content),
            )
            db.commit()
            return redirect(url_for("mail.index"))
        else:
            for error in errors:
                flash(error)

    return render_template("mails/create.html")


def send(to, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"])
