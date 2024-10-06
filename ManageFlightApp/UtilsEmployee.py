from ManageFlightApp.models import *
import hashlib


def get_list_flight():
    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    list_flight = db.session.query(
        Flight,
        Route,
        departure_airport_alias,
        arrival_airport_alias


    ).join(Route, Flight.route_id == Route.id).join(
        departure_airport_alias, Route.departure_id == departure_airport_alias.id
    ).join(
        arrival_airport_alias, Route.arrival_id == arrival_airport_alias.id
    ).all()
    return list_flight


def get_list_ticket():
        pass


def get_class():
    return db.session.query(TicketClass)


def get_detail_flight(flight_id):
    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    list_flight = (db.session.query(
        Flight,
        Route,
        departure_airport_alias,
        arrival_airport_alias,
        TicketPrice,
        Plane.name

    ).join(Route, Flight.route_id == Route.id).join(
        departure_airport_alias, Route.departure_id == departure_airport_alias.id
    ).join(
        arrival_airport_alias, Route.arrival_id == arrival_airport_alias.id
    ).join(TicketPrice, TicketPrice.flight_id == Flight.id)
                   .join(Schedules, Schedules.flight_id == flight_id)
                   .join(Plane, Schedules.plane_id == Plane.id).filter(Flight.id.__eq__(flight_id)).first())
    return list_flight


def get_stops():
    return db.session.query(Stop).filter(Flight.id.__eq__(Stop.flight_id)).all()


def get_airport_id(name):
    return db.session.query(Airport.id).filter(Airport.name.__eq__(name)).first()


def get_route(de_name, ar_name):
    de_id = get_airport_id(name=de_name)
    ar_id = get_airport_id(name=ar_name)

    return db.session.query(Route.id).filter(Route.departure_id.__eq__(de_id[0]),
                                             Route.arrival_id.__eq__(ar_id[0])).first()


def update_flight(airports, airplane):

    # route_id = get_route(de_name=airplane["departure"], ar_name=airplane["departure"])
    name = airplane["departure"] + airplane["arrival"]
    de_id = get_airport_id(name=airplane["departure"])
    ar_id = get_airport_id(name=airplane["arrival"])
    route = Route(departure_id=de_id[0], arrival_id=ar_id[0], name=name)
    flight = Flight(route=route, departure_time=airplane["time_de"], arrival_time=airplane["time_arr"],
                     quantity_class_1=airplane["rate1"], quantity_class_2=airplane["rate2"], number_of_airport=airplane["quantity_airport"])

    for i in range(1, airplane["quantity_airport"] + 1):
        id = str(i)
        a2_id = get_airport_id(airports[id]["airport"])
        stop = Stop(route=route, airport_id=a2_id[0], arrival_time=airports[id]["arr_date"], flight=flight,
                      time_delay_max=airports[id]["time_delay_max"], time_delay_min=airports[id]["time_delay_min"])
        db.session.add(stop)
        db.session.commit()



def get_list_Route():
    return db.session.query(Route).all()


def get_airport():
    return db.session.query(Airport).all()


def customer_booked_ticket():
    return db.session.query(Customer, Ticket).join(Customer, Customer.id == Ticket.customer_id).all()


def save_ticket(info):

    c = Customer(phone=info["phone"],
                 Identify=info["identify"],
                 name=info["name"], username="kien", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))

    ticket = Ticket(seat_id=2, customer=c, flight_id=info["flight_id"], ticket_class_id=info["id_class"])
    receipt = Receipt(employee_id=1,  unit_price=info["price"], customer=c)

    detail = ReceiptDetail(ticket=ticket, receipt=receipt)
    db.session.add(detail)
    db.session.commit()

