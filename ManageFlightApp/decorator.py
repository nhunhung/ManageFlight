from functools import wraps
from flask_login import login_user as flask_login_user, logout_user, current_user
from flask import render_template, redirect, request, url_for, session, jsonify
from sqlalchemy.sql.functions import user

from ManageFlightApp import controllers, employee, login, utils
from ManageFlightApp.models import UserRoleEnum, Person


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        print(f"User authenticated: {current_user.is_authenticated}")
        print(f"Current user: {current_user}")
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return check


def role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))

        if current_user.user_role != UserRoleEnum.EMPLOYEE:
            return redirect(url_for("unauthorized"))
        return f(*args, **kwargs)
    return decorated_function



load_pos = login_required(controllers.load_pos)
