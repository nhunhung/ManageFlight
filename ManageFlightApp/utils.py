from ManageFlightApp.models import *
import hashlib
from sqlalchemy import func, extract


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
    total_revenue = db.session.query(func.sum(Receipt.unit_price)).scalar()
    k = 100 / total_revenue
    return (db.session.query(Route.name, func.sum(Receipt.unit_price), func.count(Flight.id),
                             func.sum(Receipt.unit_price) * k)
            .join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id).filter(extract('month', Receipt.created_date) == m)
            .group_by(Route.name, extract('month', Receipt.created_date)).all())


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