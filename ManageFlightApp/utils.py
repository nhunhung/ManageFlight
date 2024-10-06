from sqlalchemy.engine import cursor

from ManageFlightApp.models import *
import hashlib
from sqlalchemy import func, extract, update
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy.orm import aliased


def get_user_by_id(user_id):
    return Customer.query.get(user_id)


def check_admin(username, password, role=UserRoleEnum.ADMIN):
    password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    return db.session.query(Employee).filter(Employee.username.__eq__(username.strip()),
                                             Employee.password.__eq__(password),
                                             Employee.user_role.__eq__(role)).first()


def flight_states():
    k = db.session.query(Route.name, func.count(Flight.id)).join(Flight, Route.id == Flight.route_id).group_by(
        Route.name).all()
    # import pdb
    # pdb.set_trace()
    return k


def get_user_by_id(user_id):
    return Customer.query.get(int(user_id))


def revenue_states():
    return (db.session.query(Route.name, extract('month', Receipt.created_date), func.sum(Receipt.unit_price))
            .join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id)
            .group_by(Route.name, extract('month', Receipt.created_date)).all())


def percent_states():
    total_revenue = db.session.query(func.sum(Receipt.unit_price)).scalar()
    k = 100 / total_revenue
    return db.session.query(Route.name, func.sum(Receipt.unit_price) * k).join(Flight,
                                                                               Route.id == Flight.route_id).join(
        Receipt, Flight.id == Receipt.flight_id).group_by(Route.name).all()


def General_States(m):
    return (db.session.query(Route.name, func.sum(Receipt.unit_price))
            .join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id)
            .group_by(Route.name, extract('month', Receipt.created_date))
            .filter(extract('month', Receipt.created_date) == m).all())


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Customer(username=username.strip(),
                 password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return Customer.query.filter(Customer.username.__eq__(username.strip()),
                                 Customer.password.__eq__(password)).first()


def get_all_airport_names():
    return db.session.query(Airport.id, Airport.name).all()


def get_airport_name(a):
    return db.session.query(Airport.name).filter(Airport.id.__eq__(a)).first()


def get_route(start_location, end_location):
    return (db.session.query(Route.name, Airport.location, Flight.id).join(Airport, Airport.id == Route.departure_id)
            .join(Flight, Flight.id == Route.id)
            )


def get_airport_id(f):
    return db.session.query(Airport.id).filter(Airport.name.__eq__(f)).first()


def get_flight_by_id(flight_id):
    return (db.session.query(Route.departure_id.label('departure_airport_id'),
                             Route.arrival_id.label('arrival_airport_id'),
                             Flight.departure_time.label('departure_time'),
                             Flight.arrival_time.label('arrival_time'),
                             Plane.name.label('plane_name'),
                             TicketPrice.price.label('ticket_price'),
                             TicketClass.name.label('ticket_class_name'))
            .join(Flight, Flight.route_id == Route.id)
            .join(Airport, Airport.id == Route.departure_id)
            .join(TicketPrice, Flight.id == TicketPrice.flight_id)
            .join(TicketClass, TicketPrice.ticket_class_id == TicketClass.id)
            .join(Schedules, Schedules.flight_id == flight_id)
            .join(Plane, Schedules.plane_id == Plane.id)
            .filter(Flight.id.__eq__(flight_id))
            .all()
            )


stop_alias = aliased(Stop)
airport_alias = aliased(Airport)


def get_stop_details(flight_ids):
    stop_details = (
        db.session.query(
            Stop.flight_id.label('id'),
            airport_alias.name.label('stop_airport_name'),
            Stop.arrival_time.label('stop_arrival_time'),
            Stop.time_delay_min.label('stop_delay_min'),
            Stop.order.label('stop_order')
        )
        .join(airport_alias, airport_alias.id == Stop.airport_id)
        .filter(Stop.id.in_(flight_ids))
        .order_by(Stop.order)  # Sắp xếp theo thứ tự để đảm bảo đúng thứ tự
        .all()
    )

    return stop_details


def get_flight_details(start_location, end_location, departure):
    de_id = get_airport_id(start_location)
    ar_id = get_airport_id(end_location)

    airport_alias = aliased(Airport)

    subquery = (
        db.session.query(
            Stop.flight_id.label('id'),
            func.group_concat(airport_alias.name).label('stop_airport_names'),
            func.group_concat(Stop.order).label('stop_orders')
        )
        .join(airport_alias, airport_alias.id == Stop.airport_id)
        .group_by(Stop.flight_id)
        .subquery()
    )

    result = (
        db.session.query(
            Flight.id.label('id'),
            Route.name.label('route_name'),
            TicketPrice.price.label('ticket_price'),
            Route.departure_id.label('departure_airport_id'),
            Route.arrival_id.label('arrival_airport_id'),
            Route.distance.label('distance'),
            Flight.departure_time.label('departure_time'),
            Flight.arrival_time.label('arrival_time'),
            TicketClass.name.label('ticket_class_name'),
            TicketClass.id.label('class_id'),
            Flight.number_of_airport.label('num_stops'),
            subquery.c.stop_airport_names.label('stop_airport_names'),
            subquery.c.stop_orders.label('stop_orders'),
            subquery.c.stop_orders.label('stop_arrival_time')
        )
        .join(Flight, Flight.route_id == Route.id)
        .join(Airport, Airport.id == Route.departure_id)
        .join(TicketPrice, Flight.id == TicketPrice.flight_id)
        .join(TicketClass, TicketPrice.ticket_class_id == TicketClass.id)
        .join(subquery, subquery.c.id == Flight.id)
        .filter(Route.departure_id == de_id[0],
                Route.arrival_id == ar_id[0],
                func.date_format(Flight.departure_time, '%Y-%m-%d') == departure)
        .all()
    )

    flight_ids = [row.id for row in result]
    stop_details = get_stop_details(flight_ids)

    flight_details = []

    for row in result:
        flight_id = row.id
        stop_airport_names = row.stop_airport_names.split(',')
        stop_orders = [int(order) for order in row.stop_orders.split(',')]

        stop_details_for_flight = [
            stop_detail for stop_detail in stop_details if stop_detail.id == flight_id
        ]

        stop_details_dict = {}
        for stop_detail in stop_details_for_flight:
            stop_details_dict[stop_detail.stop_order] = {
                'stop_airport_name': stop_detail.stop_airport_name,
                'stop_arrival_time': stop_detail.stop_arrival_time,
                'stop_delay_min': stop_detail.stop_delay_min
            }

        flight_details.append({
            'Flight': {
                'ID': row.id,
                'Route Name': row.route_name,
                'Ticket Price': row.ticket_price,
                'Number of Airports': row.num_stops
            },
            'Details': {
                'Điểm đi': db.session.query(Airport.name).filter(Airport.id == row.departure_airport_id).first()[
                    0],
                'Điểm đến': db.session.query(Airport.name).filter(Airport.id == row.arrival_airport_id).first()[0],
                'Ngày khởi hành': row.departure_time,
                'Ngày đến': row.arrival_time,
                'Hạng vé': row.ticket_class_name,
                'Tên sân bay trung gian': stop_airport_names,
                'Thứ tự sân bay trung gian': stop_orders,
                'Details for Stops': stop_details_dict
            }
        })

    return result


def get_seat(flight_id):
    return (db.session.query(Seat).join(Plane, Plane.id == Seat.plane_id)
            .join(Schedules, Schedules.plane_id == Plane.id)
            .join(Flight, Flight.id == Schedules.flight_id)
            .filter(Flight.id == flight_id)
            .all())


def get_seat_first(flight_id):
    return (db.session.query(Seat.id).join(Plane, Plane.id == Seat.plane_id)
            .join(Schedules, Schedules.plane_id == Plane.id)
            .join(Flight, Flight.id == Schedules.flight_id)
            .filter(Flight.id == flight_id)
            .first())


def get_list_seat(flight_id):
    return db.session.query(Flight, TicketPrice, TicketClass).join(Flight.id == TicketPrice.flight_id) \
        .join()


def save_ticket(info):
    c = Customer(phone=info["phone"],
                 Identify=info["identify"],
                 name=info["name"], username="kien", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))

    ticket = Ticket(seat_id=2, customer=c, flight_id=info["flight_id"], ticket_class_id=info["id_class"])
    receipt = Receipt(employee_id=1,flight_id=info["flight_id"], unit_price=info["price"], customer=c)

    detail = ReceiptDetail(ticket=ticket, receipt=receipt)
    update_query = update(Seat).where(Seat.id == info["id_seat"]).values(status=1)
    db.session.execute(update_query)
    db.session.add(detail)
    db.session.commit()
