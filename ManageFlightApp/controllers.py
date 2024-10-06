from functools import wraps

import cloudinary
from functools import wraps
from flask import render_template, url_for, request, redirect, session, Flask, jsonify
from cloudinary import uploader
from flask_login import login_user, logout_user, current_user
from ManageFlightApp.models import UserRoleEnum
from ManageFlightApp import app, utils, UtilsEmployee, login
import stripe


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return check


@login.user_loader
def user_loader(user_id):
    return utils.get_user_by_id(user_id=user_id)


def index():
    airport = utils.get_all_airport_names()
    return render_template('home/index.html', airport=airport)


def list_flight_booking():
    airport = utils.get_all_airport_names()

    location_from = request.form['from']
    location_to = request.form['to']
    departure = request.form["departure"]
    # import pdb
    # pdb.set_trace()

    flights = utils.get_flight_details(start_location=location_from, end_location=location_to, departure=departure)
    stops = UtilsEmployee.get_stops()
    # if flights
    # price_eco = flights
    return render_template('user/list-flight.html', airport=airport, flights=flights,
                           start=location_from, end=location_to, stops=stops)


@login_required
def load_pos():
    flight_id = request.args.get('flight_id')
    class_id = request.args.get('class_id')
    list_flight = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    list_airport = UtilsEmployee.get_airport()
    for airport in list_airport:
        if airport.id == list_flight.Route.departure_id:
            departure = airport.name
        if airport.id == list_flight.Route.arrival_id:
            arrival = airport.name

    info = {
        "flight_id": list_flight.Flight.id,
        "departure": departure,
        "arrival": arrival,
        "price": list_flight.TicketPrice.price,
        "departure_time": list_flight.Flight.departure_time,
        "arrival_time": list_flight.Flight.arrival_time,
        "class": list_flight.TicketPrice.ticket_class.name,
        "id_class": list_flight.TicketPrice.ticket_class.id,
        "plane": list_flight[5]
    }
    session["info"] = info
    # import pdb
    # pdb.set_trace()
    seats = utils.get_seat(flight_id)
    seat_first = utils.get_seat_first(flight_id)
    seat_first = int(seat_first[0])
    class_id = int(class_id)
    return render_template('user/position.html', seats=seats, seat_first=seat_first, class_id=class_id)


def api_info():
    data = request.json
    id_value = data.get('id')
    name_value = data.get('name')
    status_value = data.get('status')
    response_data = {
        'id_seat': id_value,
        'name': name_value,
        'status': status_value,
        "departure": session["info"]["departure"],
        "arrival": session["info"]["arrival"],
        "price": session["info"]["price"],
        "departure_time": session["info"]["departure_time"],
        "arrival_time": session["info"]["arrival_time"],
        "class": session["info"]["class"],
        "flight_id": session["info"]["flight_id"],
        "id_class": session["info"]["id_class"],
        "plane": session["info"]["plane"]
    }
    session['info'] = response_data
    # import pdb
    # pdb.set_trace()
    return jsonify(response_data)


def enter_flight_detail():
    response_data = {
        'id_seat': session["info"]["id_seat"],
        'name_seat': session["info"]["name"],
        'status': session["info"]["status"],
        "departure": session["info"]["departure"],
        "arrival": session["info"]["arrival"],
        "price": session["info"]["price"],
        "departure_time": session["info"]["departure_time"],
        "arrival_time": session["info"]["arrival_time"],
        "class": session["info"]["class"],
        "flight_id": session["info"]["flight_id"],
        "id_class": session["info"]["id_class"],
        "plane": session["info"]["plane"]
    }
    session['info'] = response_data
    return render_template('user/ticket-info.html')


def enter_customer_info():
    if request.method == "POST":
        name = request.form["fullname"]
        birthdate = request.form["dob"]
        phone = request.form["phone"]
        identify = request.form["id"]
        gender = request.form["gender"]
        info_user = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone,
            "identify": identify,
            "gender": gender,
            "departure": session["info"]["departure"],
            "arrival": session["info"]["arrival"],
            "price": session["info"]["price"],
            "departure_time": session["info"]["departure_time"],
            "arrival_time": session["info"]["arrival_time"],
            "class": session["info"]["class"],
            "flight_id": session["info"]["flight_id"],
            "id_class": session["info"]["id_class"],
            "plane": session["info"]["plane"],
            'id_seat': session["info"]["id_seat"],
            'name_seat': session["info"]["name_seat"],
            'status': session["info"]["status"]
        }
        session['info'] = info_user
        # import pdb
        # pdb.set_trace()
        return render_template('user/confirm.html')


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
                print('thành cong')

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template('home/register.html', err_msg=err_msg)


def ticket():
    customer_info = session.get('info', {})
    return render_template("user/ticket.html", customer_info=customer_info)


def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.auth_user(username=username, password=password)
        if user:
            # ghi nhận user đã đăng nhập ; current_user toàn cục
            login_user(user=user)
            # if "next" in request.args:
            #     return redirect(request.args["next"])
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


def payment_cus():
    try:
        utils.save_ticket(session.get("info"))
        import pdb
        pdb.set_trace()
        # client = Client(keys.account_sid, keys.auth_token)
        # client.messages.create(
        #     body="this is a sample message",
        #     from_=keys.twilio_number,
        #      to=keys.my_number)
        #
        # del session["info"]

        return jsonify({"code": 200})

    except Exception as ex:
        return jsonify({"code": 400})


def pay_online():
    return render_template("user/stripe.html")



stripe_keys = {
    "secret_key": "sk_test_51O8JTWAinse2iCe4RYF94et3W6kCV1qmyVKtRa76ehMxWhziMPkSWfsVnHyB3cCMpeVpy3VrydwVWR5VONGgIpgM007PfrYs9v",
    "publishable_key": "pk_test_51O8JTWAinse2iCe44j6W9QiJkRYJN2svgQPiFCYuUsE69LPiWHghEtd5rQxXyOsTLmvZgZ4wHEp4IbLdywLJG3is00HSIIsOo4",
    "endpoint_secret": "whsec_da47e8ca5f6706fe92bd7fb8650e41f63c847d02393b46c471e1c987d1174e7f"
}

stripe.api_key = stripe_keys["secret_key"]


def get_publishable_key():
    return jsonify({"publicKey": stripe_keys["publishable_key"]})


def create_payment_intent():
    try:

        payment_intent = stripe.PaymentIntent.create(
            amount=1099,
            currency='eur',
            automatic_payment_methods={'enabled': True}
        )
        return jsonify({'clientSecret': payment_intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': e.user_message}})


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "T-shirt",
                    "quantity": 1,
                    "currency": "usd",
                    "amount": "2000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/my-route', methods=['POST'])
def my_route():
    import pdb
    pdb.set_trace()
    return jsonify({'request': request.json})


@app.route("/webhook", methods=['POST'])
def stripe_webhook():


    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        handle_checkout_session(session)

    return 'Success', 200


def handle_checkout_session(session):
    print("Payment was successful.")
    # TODO: run some custom code here




#
# if __name__ == '__main__':
#     app.run(debug=True)