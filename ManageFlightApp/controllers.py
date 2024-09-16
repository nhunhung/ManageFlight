import cloudinary
from flask import render_template, url_for, request, redirect
from cloudinary import uploader
from flask_login import login_user, logout_user, login_required
from ManageFlightApp.models import UserRoleEnum
from ManageFlightApp import app, utils


def index():
    # airport = dao.load_airport()
    return render_template('home/index.html')


def list_flight_booking():
    # airport = dao.load_airport()
    # route = dao.load_route()

    location_from = request.args.get('from')
    location_to = request.args.get('to')
    departure = request.args.get('departure')
    # flights = dao.load_flight_booking(start_location=location_from, end_location=location_to, departure=departure)

    # if flights
    # price_eco = flights
    return render_template('home/list-flight.html')


def load_pos():
    # pos_type = dao.load_type_of_position()
    return render_template('user/position.html')


def register():
    err_msg = ''

    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:

                utils.register(username=request.form['username'],
                             password=password, avatar=avatar)
                print('thanfh cong')

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template('home/register.html', err_msg=err_msg)


def ticket():
    return render_template("ticket.html")

def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.auth_user(username=username, password=password)
        if user:
            # ghi nhận user đã đăng nhập ; current_user toàn cục
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_mgs = "Lỗi sai username hoặc password!!"
    return render_template('home/login.html', err_mgs=err_mgs)


@login_required
def logout_my_user():
    logout_user()
    return redirect('/')


def sign_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method.__eq__("POST"):

        user = utils.check_admin(username=username, password=password, role=UserRoleEnum.ADMIN)
        if user:
            login_user(user=user)

    return redirect("/admin")


if __name__ == '__main__':
    app.run(debug=True)
