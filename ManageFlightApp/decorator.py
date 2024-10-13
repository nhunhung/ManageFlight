from functools import wraps
from flask_login import login_user as flask_login_user, logout_user, current_user
from flask import render_template, redirect, request, url_for, session, jsonify

from ManageFlightApp import controllers, employee


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return check


load_pos = login_required(controllers.load_pos)

index_employee = login_required(employee.index_employee)
