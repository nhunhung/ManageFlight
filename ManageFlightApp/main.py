from flask import render_template
from ManageFlightApp import app, controllers, utils, login

app.add_url_rule("/", 'index', controllers.index)
app.add_url_rule("/register", 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/login', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/sign_admin', 'sign_admin', controllers.sign_admin, methods=['post'])
app.add_url_rule('/list-flight', 'list-flight', controllers.list_flight_booking, methods=['get'])
app.add_url_rule('/load_pos', 'load_pos', controllers.load_pos, methods=['get'])
# app.add_url_rule('/ticket', 'ticket', controllers.ticket, methods=['get'])



@app.route("/user")
def user():
    return render_template('user/index.html')

# @app.route("/login")
# def login():
#     return render_template('home/login.html')

# @app.route("/list")
# def list_flights():
#     return render_template('home/list-flight.html')

#


@app.route("/ticket")
def ticket():
    return render_template('user/ticket.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route("/account")
def account():
    return render_template('user/account.html')


@app.route("/pos")
def position():
    return render_template('user/position.html')


@app.route("/info")
def info():
    return render_template('user/ticket-info.html')


@app.route("/confirm")
def confirm():
    return render_template('user/confirm.html')

#
# @app.route("/manage-route")
# def manage_routes():
#     return render_template('admin/manage-route.html')
#
# @app.route("/manage-flight")
# def manage_flights():
#     return render_template('admin/manage-flight.html')
#
# @app.route("/manage-airplane")
# def manage_airplanes():
#     return render_template('admin/manage-airplane.html')
#
# @app.route("/manage-discount")
# def manage_discounts():
#     return render_template('admin/manage-discount.html')
#
# @app.route("/manage-pricing")
# def manage_pricings():
#     return render_template('admin/manage-pricing.html')
#
# @app.route("/manage-account")
# def manage_accounts():
#     return render_template('admin/manage-account.html')
#
# @app.route("/manage-booking")
# def manage_bookings():
#     return render_template('admin/manage-booking.html')
#
# @app.route("/manage-payment")
# def manage_payments():
#     return render_template('admin/manage-payment.html')
#
# @app.route("/manage-type-of-position")
# def manage_type_of_positions():
#     return render_template('admin/manage-type-of-position.html')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from ManageFlightApp.admin import *

    app.run(debug=True)
