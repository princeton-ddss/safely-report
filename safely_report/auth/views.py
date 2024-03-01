from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_required, login_user

from safely_report.auth.utils import logout_and_clear, make_auth_form
from safely_report.models import Role, User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/")
def index():
    return render_template("auth/index.html")


@auth_blueprint.route("/login/respondent", methods=["GET", "POST"])
def login_respondent():
    form = make_auth_form("Please enter your UUID:")
    form.meta.update_values({"back_url": url_for("auth.index")})

    if form.validate_on_submit():
        uuid = form.field.data
        user = User.query.filter_by(uuid=uuid).first()
        if user is not None and user.role == Role.Respondent:
            login_user(user)
            current_app.logger.info(f"Login - user {user.id}")
            return redirect(url_for("survey.index"))
        current_app.logger.warning("Failed respondent login")
        flash("Respondent not found", "error")
        return redirect(url_for("auth.login_respondent"))

    return render_template("auth/submit.html", form=form)


@auth_blueprint.route("/login/enumerator", methods=["GET", "POST"])
def login_enumerator():
    form = make_auth_form("Please enter your UUID:")
    form.meta.update_values({"back_url": url_for("auth.index")})

    if form.validate_on_submit():
        uuid = form.field.data
        user = User.query.filter_by(uuid=uuid).first()
        if user is not None and user.role == Role.Enumerator:
            login_user(user)
            current_app.logger.info(f"Login - user {user.id}")
            return redirect(url_for("enumerator.index"))
        current_app.logger.warning("Failed enumerator login")
        flash("Enumerator not found", "error")
        return redirect(url_for("auth.login_enumerator"))

    return render_template("auth/submit.html", form=form)


@auth_blueprint.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    form = make_auth_form("Please enter admin password:")
    form.meta.update_values({"back_url": url_for("auth.index")})

    if form.validate_on_submit():
        password = form.field.data
        if password == current_app.config["ADMIN_PASSWORD"]:
            user = User.get_admin()
            login_user(user)
            current_app.logger.info(f"Login - user {user.id}")
            return redirect(url_for("admin.index"))
        current_app.logger.warning("Failed admin login")
        flash("Invalid password", "error")
        return redirect(url_for("auth.login_admin"))

    return render_template("auth/submit.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    id = current_user.id
    logout_and_clear()
    current_app.logger.info(f"Logout - user {id}")
    return redirect(url_for("auth.index"))
