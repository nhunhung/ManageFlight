from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, BOOLEAN, ForeignKey, FLOAT, DATETIME, func
from sqlalchemy.orm import relationship
from ManageFlightApp import Admin, db, app
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class Person(db.Model, UserMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class Customer(Person):
    phone = Column(String(12), nullable=True)
    Identify = Column(String(20), nullable=True)
    receipts = relationship("Receipt", backref="customer", lazy=True)


class Employee(Person):
    salary = Column(FLOAT, nullable=True)


class Seat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_seat = Column(String(255), nullable=True)
    status = Column(BOOLEAN, default=False)
    plane_id = Column(Integer, ForeignKey('plane.id'), nullable=False)
    plane_seat = relationship('Plane', backref='seat', lazy=True)


class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)
    departure_time = Column(DATETIME)
    arrival_time = Column(DATETIME)
    flight_ticket = relationship('Ticket', backref='flight', lazy=True)


class TicketClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)  # Số lượng hạng vé


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_time = Column(DATETIME, nullable=False, default=datetime.now())  # Thời gian mua vé
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    fight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)


class Plane(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DATETIME, default=datetime.now())
    user_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    quantity = Column(Integer, default=0)
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    unit_price = Column(FLOAT, default=0)

    detail_receipt = relationship("ReceiptDetail", backref="receipt", lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), primary_key=True, nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True, nullable=False)


class Schedules(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    plane_id = Column(Integer, ForeignKey(Plane.id), primary_key=True, nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True, nullable=False)


class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên sân bay
    location = Column(String(255))  # Địa điểm sân bay
    stops_airport = relationship('Stop', backref='airport', lazy=True)


class Route(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên của tuyến đường
    distance = Column(FLOAT)  # Khoảng cách của tuyến đường (đơn vị: km)
    number_of_airport = Column(Integer, nullable=False)
    arrival_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # diểm đến
    departure_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # điểm đi
    stops_route = relationship('Stop', backref='route', lazy=True)


class TicketPrice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(FLOAT, default=0)  # Đơn giá vé
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)


class Stop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # Khóa ngoại liên kết với sân bay
    arrival_time = Column(DATETIME)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)  # Khóa ngoại liên kết với tuyến đường
    order = Column(Integer)  # Thứ tự của điểm dừng trên tuyến đường
    time_delay_max = Column(FLOAT)  # Thời gian Đếm
    time_delay_min = Column(FLOAT)  # Thời gian khởi hành


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        # u1 = Employee(name='Admin', username='admin',
        #               password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), salary=50000000,
        #               user_role=UserRoleEnum.ADMIN)
        #
        # u2 = Customer(name='Nguyễn Trung Kiên', username='TrungKienIdol',
        #               password=str(hashlib.md5('TrungKien123'.encode('utf-8')).hexdigest()))
        # u3 = Customer(name='Hồ Ngọc Nhung', username='NhungNgoc',
        #               password=str(hashlib.md5('NhungNgoc123'.encode('utf-8')).hexdigest()))
        # u4 = Customer(name='Bùi Mỹ Nhân', username='ManNhi',
        #               password=str(hashlib.md5('ManNhi123'.encode('utf-8')).hexdigest()))
        # u5 = Customer(name='Tống Thị Thu Hiền', username='ThuHien',
        #               password=str(hashlib.md5('ThuHien123'.encode('utf-8')).hexdigest()))
        # u6 = Customer(name='Huỳnh Trúc Ly', username='TrucLy',
        #               password=str(hashlib.md5('TrucLy2003'.encode('utf-8')).hexdigest()))
        # u7 = Customer(name='Duong Thi Hong Nhu', username='HongNhu',
        #               password=str(hashlib.md5('HongNhu2004'.encode('utf-8')).hexdigest()))
        # u8 = Customer(name='Nguyễn Cao', username='CaoNguyen',
        #               password=str(hashlib.md5('CaoNguyen123'.encode('utf-8')).hexdigest()))
        # u9 = Employee(name='Phương Mỹ Chi', username='MyChi',
        #               password=str(hashlib.md5('MyChi123'.encode('utf-8')).hexdigest()), salary=10000000,
        #               user_role=UserRoleEnum.EMPLOYEE)
        # u10 = Employee(name='Hồ Thị Cẩm', username='ThiCam',
        #                password=str(hashlib.md5('ThiCam123'.encode('utf-8')).hexdigest()), salary=15000000,
        #                user_role=UserRoleEnum.EMPLOYEE)
        #
        # db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
        # db.session.commit()
        #
        # k1 = TicketClass(name='Hang Pho Thong', quantity=15)
        # k2 = TicketClass(name='Hang Thuong Gia', quantity=10)
        #
        # db.session.add_all([k1, k2])
        # db.session.commit()
        #
        # A1 = Airport(name='TP.HCM', location='Bình Thạnh, Thành phố Hồ Chí Minh')
        # A2 = Airport(name='Hà Nội', location='Linh Xuân, Hà Nội')
        # A3 = Airport(name='Hải Phòng', location='Đóng Đa, Hải Phòng')
        # A4 = Airport(name='Đà Nẵng', location='Hiệp Phước, Đà Nẵng')
        # A5 = Airport(name='Cà Mau', location='Long Mỹ, Cà Mau')
        # A6 = Airport(name='Tây Ninh', location='Châu Thanh, Tây Ninh')
        # A7 = Airport(name='Sapa', location='Phnong, Sapa')
        # A8 = Airport(name='Đà Lạt', location='67, Đà Lạt')
        # A9 = Airport(name='Vũng Tàu', location='Xô Viết, Vũng tàu')
        # A10 = Airport(name='Phan Thiết', location='Trần Hưng Đạo, Phan Thiết')
        # a11 = Airport(name='Hà Giang', location='Bình Thạnh, Hà Giang')
        #
        # db.session.add_all([A1, A2, A3, A4, A5, A6, A7, A8, A9, A10])
        # db.session.commit()
        #
        # r1 = Route(name='TP.HCM - HÀ NỘI', distance=1190, number_of_airport=2, arrival_id=2, departure_id=1)
        # r2 = Route(name='TP.HCM - Đà Nẵng', distance=590, number_of_airport=0, arrival_id=4, departure_id=1)
        # r3 = Route(name='Đà Nẵng - Hải Phòng', distance=200, number_of_airport=0, arrival_id=3, departure_id=4)
        # r4 = Route(name='Hải Phòng - HÀ NỘI', distance=400, number_of_airport=0, arrival_id=2, departure_id=3)
        # r5 = Route(name='TP.HCM - Cà Mau', distance=1190, number_of_airport=2, arrival_id=5, departure_id=1)
        # r6 = Route(name='SaPa - Phan thiết', distance=1190, number_of_airport=1, arrival_id=10, departure_id=7)
        # r7 = Route(name='Phan Thiết - Vũng tàu', distance=1190, number_of_airport=0, arrival_id=9, departure_id=10)
        # r8 = Route(name='Tây Ninh - Sapa', distance=1190, number_of_airport=2, arrival_id=7, departure_id=6)
        # r9 = Route(name='Đà Lạt - TP.HCM', distance=1190, number_of_airport=0, arrival_id=1, departure_id=8)
        # r10 = Route(name='Vũng Tàu - Đà Lạt', distance=1190, number_of_airport=0, arrival_id=8, departure_id=9)
        # r11 = Route(name='Đà nẵng - Đà Lạt', distance=1190, number_of_airport=0, arrival_id=8, departure_id=9)
        #
        # db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10])
        # db.session.commit()
        #
        # St1 = Stop(route_id=1, airport_id=4, order=1, arrival_time='2023-12-31 11:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St2 = Stop(route_id=1, airport_id=3, order=2, arrival_time='2023-12-31 14:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St3 = Stop(route_id=6, airport_id=10, order=1, arrival_time='2023-12-31 13:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St = Stop(route=r11, airport=a11, arrival_time='2023-12-31 20:00:00', time_delay_max=30, time_delay_min=20)
        # St4 = Stop(route_id=8, airport_id=10, order=1, arrival_time='2023-12-1 01:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St5 = Stop(route_id=8, airport_id=4, order=1, arrival_time='2023-12-1 04:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St6 = Stop(route_id=9, airport_id=4, order=1, arrival_time='2023-12-31 09:00:00', time_delay_max=30,
        #            time_delay_min=20)
        # St7 = Stop(route_id=6, airport_id=4, order=1, arrival_time='2023-12-31 21:00:00', time_delay_max=30,
        #            time_delay_min=20)
        #
        #
        # db.session.add_all([St4, St5, St6, St7])
        # db.session.commit()
        #
        # db.session.add_all([St1, St2, St3, St, St4, St5, St6, St7])
        # db.session.commit()
        #
        # p1 = Plane(name='Máy bay 1')
        # p2 = Plane(name='Máy bay 2')
        # p3 = Plane(name='Máy bay 3')
        # p4 = Plane(name='Máy bay 4')
        # p5 = Plane(name='Máy bay 5')
        # p6 = Plane(name='Máy bay 6')
        # p7 = Plane(name='Máy bay 7')
        # p8 = Plane(name='Máy bay 8')
        # p9 = Plane(name='Máy bay 9')
        # p10 = Plane(name='Máy bay 10')
        #
        # db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
        # db.session.commit()
        #
        # S1 = Seat(number_seat='A01', plane_id=1, status=True)
        # S2 = Seat(number_seat='A02', plane_id=1, status=True)
        # S3 = Seat(number_seat='A03', plane_id=1, status=True)
        # S4 = Seat(number_seat='A04', plane_id=1)
        # S5 = Seat(number_seat='A05', plane_id=1)
        # S6 = Seat(number_seat='A06', plane_id=1)
        # S7 = Seat(number_seat='A07', plane_id=1)
        # S8 = Seat(number_seat='A08', plane_id=1)
        # S9 = Seat(number_seat='A09', plane_id=1)
        # S10 = Seat(number_seat='A010', plane_id=1)
        # S11 = Seat(number_seat='A011', plane_id=1)
        # S12 = Seat(number_seat='A012', plane_id=1)
        # S13 = Seat(number_seat='A013', plane_id=1)
        # S14 = Seat(number_seat='A014', plane_id=1)
        # S15 = Seat(number_seat='A015', plane_id=1)
        # S16 = Seat(number_seat='B01', plane_id=1, status=True)
        # S17 = Seat(number_seat='B02', plane_id=1, status=True)
        # S18 = Seat(number_seat='B03', plane_id=1, status=True)
        # S19 = Seat(number_seat='B04', plane_id=1, status=True)
        # S20 = Seat(number_seat='B05', plane_id=1)
        # S21 = Seat(number_seat='B06', plane_id=1, )
        # S22 = Seat(number_seat='B07', plane_id=1)
        # S23 = Seat(number_seat='B08', plane_id=1)
        # S24 = Seat(number_seat='B09', plane_id=1)
        # S25 = Seat(number_seat='B10', plane_id=1)
        #
        # db.session.add_all(
        #     [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
        #      S24, S25])
        # db.session.commit()
        #
        # f1 = Flight(route_id=1, departure_time='2023-12-31 9:00:00', arrival_time='2023-12-31 17:00:00')
        # f2 = Flight(route_id=8, departure_time='2023-1-31 13:30:00', arrival_time='2024-02-1 01:00:00')
        #
        # db.session.add_all([f1, f2])
        # db.session.commit()
        #
        # Rc1 = Receipt(created_date='2023-12-30 09:45:00', user_id=1, ticket_class_id=1, flight_id=1, quantity=3,
        #               unit_price=3600000)
        # Rc2 = Receipt(created_date='2023-12-30 19:15:00', user_id=2, ticket_class_id=2, flight_id=1, quantity=2,
        #               unit_price=3000000)
        # Rc3 = Receipt(created_date='2023-12-22 21:10:00', user_id=3, ticket_class_id=2, flight_id=1, quantity=2,
        #               unit_price=3000000)
        #
        # Rc1 = Receipt(created_date='2023-12-30 09:45:00', user_id=1, employee_id=2, ticket_class_id=1, flight_id=1,
        #               quantity=3,
        #               unit_price=3600000)
        # Rc2 = Receipt(created_date='2023-12-30 19:15:00', user_id=2, employee_id=2, ticket_class_id=2, flight_id=1,
        #               quantity=2,
        #               unit_price=3000000)
        # Rc3 = Receipt(created_date='2023-12-22 21:10:00', user_id=3, employee_id=2, ticket_class_id=2, flight_id=1,
        #               quantity=2,
        #               unit_price=3000000)
        #
        # db.session.add_all([Rc1, Rc2, Rc3])
        # db.session.commit()
        #
        # Tp1 = TicketPrice(price=1200000, ticket_class_id=1, flight_id=1)
        # Tp2 = TicketPrice(price=1500000, ticket_class_id=2, flight_id=1)
        #
        # Tp3 = TicketPrice(price=1700000, ticket_class_id=1, flight_id=2)
        # Tp4 = TicketPrice(price=2200000, ticket_class_id=2, flight_id=2)
        # db.session.add_all([Tp1, Tp2, Tp3, Tp4])
        # db.session.commit()
        #
        # db.session.add_all([Tp1, Tp2, Tp3, Tp4])
        # db.session.commit()

        # T1 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, fight_id=1, ticket_class_id=1)
        # T2 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, fight_id=1, ticket_class_id=1)
        # T3 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, fight_id=1, ticket_class_id=1)
        # T4 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, fight_id=1, ticket_class_id=1)
        # T5 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, fight_id=1, ticket_class_id=1)
        # T6 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, fight_id=1, ticket_class_id=1)
        # T7 = Ticket(purchase_time='2023-12-31 03:0:00', seat_id=19, fight_id=1, ticket_class_id=1)
        #
        # db.session.add_all([T1, T2, T3, T4, T5, T6, T7])
        # db.session.commit()
        #
        # rcd1 = ReceiptDetail(ticket_id=1, receipt_id=1)
        # rcd2 = ReceiptDetail(ticket_id=2, receipt_id=1)
        # rcd3 = ReceiptDetail(ticket_id=3, receipt_id=1)
        # rcd4 = ReceiptDetail(ticket_id=4, receipt_id=2)
        # rcd5 = ReceiptDetail(ticket_id=5, receipt_id=2)
        # rcd6 = ReceiptDetail(ticket_id=6, receipt_id=3)
        # rcd7 = ReceiptDetail(ticket_id=7, receipt_id=3)
        #
        # db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        # db.session.commit()
        #
        # Sc1 = Schedules(plane_id=1, flight_id=1)
        # Sc2 = Schedules(plane_id=2, flight_id=1)
        # Sc3 = Schedules(plane_id=3, flight_id=1)
        #
        # db.session.add_all([Sc1, Sc2, Sc3])
        # db.session.commit()

        # total_unit_price = db.session.query(func.sum(Receipt.unit_price)).scalar()
        #
        # print(f'Total Unit Price in Receipts: {total_unit_price}')
