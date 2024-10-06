from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, BOOLEAN, ForeignKey, FLOAT, DATETIME, func, extract
from sqlalchemy.orm import relationship, aliased
from ManageFlightApp import Admin, db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class Airline(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    quantity_airport = Column(Integer, default=10)


class Person(db.Model, UserMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class Customer(Person):
    phone = Column(String(12), nullable=True)
    Identify = Column(String(20), nullable=True)
    receipts = relationship("Receipt", backref="customer", lazy=True)
    ticket_customer = relationship("Ticket", backref="customer", lazy=True)


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
    quantity_class_1 = Column(Integer, default=15)
    quantity_class_2 = Column(Integer, default=10)
    flight_ticket = relationship('Ticket', backref='flight', lazy=True)
    number_of_airport = Column(Integer, nullable=False)
    flight_stop = relationship('Stop', backref='flight', lazy=True)


class TicketClass(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    ticket_class_price = relationship("TicketPrice", backref="ticket_class", lazy=True)


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_time = Column(DATETIME, nullable=False, default=datetime.now())  # Thời gian mua vé
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    detail_ticket = relationship("ReceiptDetail", backref="ticket", lazy=True)


class Plane(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    # flight_id = relationship('Flight', backref='plane', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DATETIME, default=datetime.now())
    user_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id))
    quantity = Column(Integer, default=0)
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
    airline_id = Column(Integer, ForeignKey(Airline.id), primary_key=True, default=1)


class Route(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Tên của tuyến đường
    distance = Column(FLOAT)  # Khoảng cách của tuyến đường (đơn vị: km)
    flight_time_min = Column(FLOAT)
    arrival_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # diểm đến
    departure_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # điểm đi
    stops_route = relationship('Stop', backref='route', lazy=True)
    route_flight = relationship('Flight', backref='route', lazy=True)


class TicketPrice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(FLOAT, default=0)  # Đơn giá vé
    ticket_class_id = Column(Integer, ForeignKey(TicketClass.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)


class Stop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)  # Khóa ngoại liên kết với sân bay
    arrival_time = Column(DATETIME, nullable=True)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)  # Khóa ngoại liên kết với tuyến đường
    order = Column(Integer)  # Thứ tự của điểm dừng trên tuyến đường
    time_delay_max = Column(FLOAT)  # Thời gian Đếm
    time_delay_min = Column(FLOAT)  # Thời gian khởi hành


if __name__ == '__main__':
    with (app.app_context()):
        db.create_all()


        import hashlib

        u1 = Employee(name='Admin', username='admin',
                      password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), salary=50000000,
                      user_role=UserRoleEnum.ADMIN)

        u2 = Customer(name='Nguyễn Trung Kiên', username='TrungKienIdol',
                      password=str(hashlib.md5('TrungKien123'.encode('utf-8')).hexdigest()))
        u3 = Customer(name='Hồ Ngọc Nhung', username='NhungNgoc',
                      password=str(hashlib.md5('NhungNgoc123'.encode('utf-8')).hexdigest()))
        u4 = Customer(name='Bùi Mỹ Nhân', username='ManNhi',
                      password=str(hashlib.md5('ManNhi123'.encode('utf-8')).hexdigest()))
        u5 = Customer(name='Tống Thị Thu Hiền', username='ThuHien',
                      password=str(hashlib.md5('ThuHien123'.encode('utf-8')).hexdigest()))
        u6 = Customer(name='Huỳnh Trúc Ly', username='TrucLy',
                      password=str(hashlib.md5('TrucLy2003'.encode('utf-8')).hexdigest()))
        u7 = Customer(name='Duong Thi Hong Nhu', username='HongNhu',
                      password=str(hashlib.md5('HongNhu2004'.encode('utf-8')).hexdigest()))
        u8 = Customer(name='Nguyễn Cao', username='CaoNguyen',
                      password=str(hashlib.md5('CaoNguyen123'.encode('utf-8')).hexdigest()))
        u9 = Employee(name='Phương Mỹ Chi', username='MyChi',
                      password=str(hashlib.md5('MyChi123'.encode('utf-8')).hexdigest()), salary=10000000,
                      user_role=UserRoleEnum.EMPLOYEE)
        u10 = Employee(name='Hồ Thị Cẩm', username='ThiCam',
                       password=str(hashlib.md5('ThiCam123'.encode('utf-8')).hexdigest()), salary=15000000,
                       user_role=UserRoleEnum.EMPLOYEE)

        db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
        db.session.commit()

        k1 = TicketClass(name='Hang Pho Thong')
        k2 = TicketClass(name='Hang Thuong Gia')

        db.session.add_all([k1, k2])
        db.session.commit()

        al = Airline(name="Sugar Glider", quantity_airport=10)

        db.session.add_all([al])
        db.session.commit()

        A1 = Airport(name='TP.HCM', location='Bình Thạnh, Thành phố Hồ Chí Minh')
        A2 = Airport(name='Hà Nội', location='Linh Xuân, Hà Nội')
        A3 = Airport(name='Hải Phòng', location='Đóng Đa, Hải Phòng')
        A4 = Airport(name='Đà Nẵng', location='Hiệp Phước, Đà Nẵng')
        A5 = Airport(name='Cà Mau', location='Long Mỹ, Cà Mau')
        A6 = Airport(name='Tây Ninh', location='Châu Thanh, Tây Ninh')
        A7 = Airport(name='Sapa', location='Phnong, Sapa')
        A8 = Airport(name='Đà Lạt', location='67, Đà Lạt')
        A9 = Airport(name='Vũng Tàu', location='Xô Viết, Vũng tàu')
        A10 = Airport(name='Phan Thiết', location='Trần Hưng Đạo, Phan Thiết')
        a11 = Airport(name='Hà Giang', location='Bình Thạnh, Hà Giang')

        db.session.add_all([A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, a11])
        db.session.commit()

        p1 = Plane(name='VN001')
        p2 = Plane(name='VN002')
        p3 = Plane(name='VN003')
        p4 = Plane(name='VN004')
        p5 = Plane(name='VN005')
        p6 = Plane(name='VN006')
        p7 = Plane(name='VN007')
        p8 = Plane(name='VN008')
        p9 = Plane(name='VN009')

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9])
        db.session.commit()

        S1 = Seat(number_seat='A01', plane_id=1, status=True)
        S2 = Seat(number_seat='A02', plane_id=1, status=True)
        S3 = Seat(number_seat='A03', plane_id=1, status=True)
        S4 = Seat(number_seat='A04', plane_id=1)
        S5 = Seat(number_seat='A05', plane_id=1)
        S6 = Seat(number_seat='A06', plane_id=1)
        S7 = Seat(number_seat='A07', plane_id=1)
        S8 = Seat(number_seat='A08', plane_id=1)
        S9 = Seat(number_seat='A09', plane_id=1)
        S10 = Seat(number_seat='A010', plane_id=1)
        S11 = Seat(number_seat='A011', plane_id=1)
        S12 = Seat(number_seat='A012', plane_id=1)
        S13 = Seat(number_seat='A013', plane_id=1)
        S14 = Seat(number_seat='A014', plane_id=1)
        S15 = Seat(number_seat='A015', plane_id=1)
        S16 = Seat(number_seat='B01', plane_id=1, status=True)
        S17 = Seat(number_seat='B02', plane_id=1, status=True)
        S18 = Seat(number_seat='B03', plane_id=1, status=True)
        S19 = Seat(number_seat='B04', plane_id=1, status=True)
        S20 = Seat(number_seat='B05', plane_id=1)
        S21 = Seat(number_seat='B06', plane_id=1, )
        S22 = Seat(number_seat='B07', plane_id=1)
        S23 = Seat(number_seat='B08', plane_id=1)
        S24 = Seat(number_seat='B09', plane_id=1)
        S25 = Seat(number_seat='B10', plane_id=1)

        db.session.add_all(
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
             S24, S25])
        db.session.commit()

        S1 = Seat(number_seat='A01', plane_id=2, status=True)
        S2 = Seat(number_seat='A02', plane_id=2, status=True)
        S3 = Seat(number_seat='A03', plane_id=2, status=True)
        S4 = Seat(number_seat='A04', plane_id=2)
        S5 = Seat(number_seat='A05', plane_id=2)
        S6 = Seat(number_seat='A06', plane_id=2)
        S7 = Seat(number_seat='A07', plane_id=2)
        S8 = Seat(number_seat='A08', plane_id=2)
        S9 = Seat(number_seat='A09', plane_id=2)
        S10 = Seat(number_seat='A010', plane_id=2)
        S11 = Seat(number_seat='A011', plane_id=2)
        S12 = Seat(number_seat='A012', plane_id=2)
        S13 = Seat(number_seat='A013', plane_id=2)
        S14 = Seat(number_seat='A014', plane_id=2)
        S15 = Seat(number_seat='A015', plane_id=2)
        S16 = Seat(number_seat='B01', plane_id=2, status=True)
        S17 = Seat(number_seat='B02', plane_id=2, status=True)
        S18 = Seat(number_seat='B03', plane_id=2, status=True)
        S19 = Seat(number_seat='B04', plane_id=2, status=True)
        S20 = Seat(number_seat='B05', plane_id=2)
        S21 = Seat(number_seat='B06', plane_id=2)
        S22 = Seat(number_seat='B07', plane_id=2)
        S23 = Seat(number_seat='B08', plane_id=2)
        S24 = Seat(number_seat='B09', plane_id=2)
        S25 = Seat(number_seat='B10', plane_id=2)

        db.session.add_all(
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
             S24, S25])
        db.session.commit()

        S1 = Seat(number_seat='A01', plane_id=3, status=True)
        S2 = Seat(number_seat='A02', plane_id=3, status=True)
        S3 = Seat(number_seat='A03', plane_id=3, status=True)
        S4 = Seat(number_seat='A04', plane_id=3)
        S5 = Seat(number_seat='A05', plane_id=3)
        S6 = Seat(number_seat='A06', plane_id=3)
        S7 = Seat(number_seat='A07', plane_id=3)
        S8 = Seat(number_seat='A08', plane_id=3)
        S9 = Seat(number_seat='A09', plane_id=3)
        S10 = Seat(number_seat='A010', plane_id=3)
        S11 = Seat(number_seat='A011', plane_id=3)
        S12 = Seat(number_seat='A012', plane_id=3)
        S13 = Seat(number_seat='A013', plane_id=3)
        S14 = Seat(number_seat='A014', plane_id=3)
        S15 = Seat(number_seat='A015', plane_id=3)
        S16 = Seat(number_seat='B01', plane_id=3, status=True)
        S17 = Seat(number_seat='B02', plane_id=3, status=True)
        S18 = Seat(number_seat='B03', plane_id=3, status=True)
        S19 = Seat(number_seat='B04', plane_id=3, status=True)
        S20 = Seat(number_seat='B05', plane_id=3)
        S21 = Seat(number_seat='B06', plane_id=3)
        S22 = Seat(number_seat='B07', plane_id=3)
        S23 = Seat(number_seat='B08', plane_id=3)
        S24 = Seat(number_seat='B09', plane_id=3)
        S25 = Seat(number_seat='B10', plane_id=3)

        db.session.add_all(
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
             S24, S25])
        db.session.commit()

        S1 = Seat(number_seat='A01', plane_id=4, status=True)
        S2 = Seat(number_seat='A02', plane_id=4, status=True)
        S3 = Seat(number_seat='A03', plane_id=4, status=True)
        S4 = Seat(number_seat='A04', plane_id=4)
        S5 = Seat(number_seat='A05', plane_id=4)
        S6 = Seat(number_seat='A06', plane_id=4)
        S7 = Seat(number_seat='A07', plane_id=4)
        S8 = Seat(number_seat='A08', plane_id=4)
        S9 = Seat(number_seat='A09', plane_id=4)
        S10 = Seat(number_seat='A010', plane_id=4)
        S11 = Seat(number_seat='A011', plane_id=4)
        S12 = Seat(number_seat='A012', plane_id=4)
        S13 = Seat(number_seat='A013', plane_id=4)
        S14 = Seat(number_seat='A014', plane_id=4)
        S15 = Seat(number_seat='A015', plane_id=4)
        S16 = Seat(number_seat='B01', plane_id=4, status=True)
        S17 = Seat(number_seat='B02', plane_id=4, status=True)
        S18 = Seat(number_seat='B03', plane_id=4, status=True)
        S19 = Seat(number_seat='B04', plane_id=4, status=True)
        S20 = Seat(number_seat='B05', plane_id=4)
        S21 = Seat(number_seat='B06', plane_id=4)
        S22 = Seat(number_seat='B07', plane_id=4)
        S23 = Seat(number_seat='B08', plane_id=4)
        S24 = Seat(number_seat='B09', plane_id=4)
        S25 = Seat(number_seat='B10', plane_id=4)

        db.session.add_all(
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
             S24, S25])
        db.session.commit()

        S1 = Seat(number_seat='A01', plane_id=5, status=True)
        S2 = Seat(number_seat='A02', plane_id=5, status=True)
        S3 = Seat(number_seat='A03', plane_id=5, status=True)
        S4 = Seat(number_seat='A04', plane_id=5)
        S5 = Seat(number_seat='A05', plane_id=5)
        S6 = Seat(number_seat='A06', plane_id=5)
        S7 = Seat(number_seat='A07', plane_id=5)
        S8 = Seat(number_seat='A08', plane_id=5)
        S9 = Seat(number_seat='A09', plane_id=5)
        S10 = Seat(number_seat='A010', plane_id=5)
        S11 = Seat(number_seat='A011', plane_id=5)
        S12 = Seat(number_seat='A012', plane_id=5)
        S13 = Seat(number_seat='A013', plane_id=5)
        S14 = Seat(number_seat='A014', plane_id=5)
        S15 = Seat(number_seat='A015', plane_id=5)
        S16 = Seat(number_seat='B01', plane_id=5, status=True)
        S17 = Seat(number_seat='B02', plane_id=5, status=True)
        S18 = Seat(number_seat='B03', plane_id=5, status=True)
        S19 = Seat(number_seat='B04', plane_id=5, status=True)
        S20 = Seat(number_seat='B05', plane_id=5)
        S21 = Seat(number_seat='B06', plane_id=5)
        S22 = Seat(number_seat='B07', plane_id=5)
        S23 = Seat(number_seat='B08', plane_id=5)
        S24 = Seat(number_seat='B09', plane_id=5)
        S25 = Seat(number_seat='B10', plane_id=5)

        db.session.add_all(
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23,
             S24, S25])
        db.session.commit()

        r1 = Route(name='TP.HCM - HÀ NỘI', distance=1190, flight_time_min=8,
                   arrival_id=2, departure_id=1)
        r2 = Route(name='TP.HCM - Đà Nẵng', distance=590, flight_time_min=8,
                   arrival_id=4, departure_id=1)
        r3 = Route(name='Đà Nẵng - Hải Phòng', distance=200, flight_time_min=8,
                   arrival_id=3, departure_id=4)
        r4 = Route(name='Hải Phòng - HÀ NỘI', distance=400, flight_time_min=8,
                   arrival_id=2, departure_id=3)
        r5 = Route(name='TP.HCM - Cà Mau', distance=1190, flight_time_min=8,
                   arrival_id=5, departure_id=1)
        r6 = Route(name='SaPa - Phan thiết', distance=1190, flight_time_min=5,
                   arrival_id=10, departure_id=7)
        r7 = Route(name='Phan Thiết - Vũng tàu', distance=1190, flight_time_min=8,
                   arrival_id=9, departure_id=10)
        r8 = Route(name='Tây Ninh - Sapa', distance=1190, flight_time_min=10,
                   arrival_id=7, departure_id=6)
        r9 = Route(name='Đà Lạt - TP.HCM', distance=1190, flight_time_min=8,
                   arrival_id=1, departure_id=8)
        r10 = Route(name='Vũng Tàu - Đà Lạt', distance=1190, flight_time_min=8,
                    arrival_id=8, departure_id=9)
        r11 = Route(name='Đà nẵng - Đà Lạt', distance=1190, flight_time_min=8,
                    arrival_id=8, departure_id=9)

        db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11])
        db.session.commit()

        f1 = Flight(route_id=1, departure_time='2024-1-31 9:00:00', number_of_airport=2,
                    arrival_time='2024-1-31 17:00:00')
        f2 = Flight(route_id=8, departure_time='2023-1-31 13:30:00', number_of_airport=2,
                    arrival_time='2024-02-1 23:30:00')
        f3 = Flight(route_id=6, departure_time='2024-2-20 18:00:00', number_of_airport=1,
                    arrival_time='2024-2-20 23:00:00')
        f4 = Flight(route_id=1, departure_time='2024-1-31 10:00:00', number_of_airport=2,
                    arrival_time='2024-1-31 19:00:00')
        f5 = Flight(route_id=1, departure_time='2024-1-20 9:00:00', number_of_airport=2,
                    arrival_time='2024-1-8 17:00:00')
        f6 = Flight(route_id=8, departure_time='2023-12-31 9:00:00', number_of_airport=2,
                    arrival_time='2023-12-31 19:00:00')
        f7 = Flight(route_id=1, departure_time='2023-12-31 2:00:00', number_of_airport=2,
                    arrival_time='2023-12-31 11:00:00')
        f8 = Flight(route_id=11, departure_time='2024-1-20 9:00:00', number_of_airport=0,
                    arrival_time='2024-1-8 17:00:00')

        db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])
        db.session.commit()

        St1 = Stop(route_id=1, airport_id=4, order=1, arrival_time='2024-1-31 11:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=1)
        St2 = Stop(route_id=1, airport_id=3, order=2, arrival_time='2024-1-31 14:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=1)

        St3 = Stop(route_id=1, airport_id=4, order=1, arrival_time='2024-1-31 13:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=4)
        St4 = Stop(route_id=1, airport_id=3, order=2, arrival_time='2024-1-31 17:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=4)

        St5 = Stop(route_id=1, airport_id=4, order=1, arrival_time='2024-1-20 11:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=5)
        St6 = Stop(route_id=1, airport_id=3, order=2, arrival_time='2024-1-20 14:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=5)

        St7 = Stop(route_id=1, airport_id=4, order=1, arrival_time='2023-12-31 5:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=7)
        St8 = Stop(route_id=1, airport_id=3, order=2, arrival_time='2023-12-31 8:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=7)

        St10 = Stop(route_id=8, airport_id=9, order=1, arrival_time='2023-1-31 16:00:00', time_delay_max=30,
                    time_delay_min=20, flight_id=2)
        St12 = Stop(route_id=8, airport_id=10, order=2, arrival_time='2023-1-31 20:00:00', time_delay_max=30,
                    time_delay_min=20, flight_id=2)

        St13 = Stop(route_id=8, airport_id=9, order=1, arrival_time='2024-2-20 12:00:00', time_delay_max=30,
                    time_delay_min=20, flight_id=6)
        St14 = Stop(route_id=8, airport_id=10, order=2, arrival_time='2024-2-20 16:00:00', time_delay_max=30,
                    time_delay_min=20, flight_id=6)

        St9 = Stop(route_id=6, airport_id=10, order=1, arrival_time='2024-2-20 20:00:00', time_delay_max=30,
                   time_delay_min=20, flight_id=3)

        db.session.add_all([St1, St2, St3, St4, St5, St6, St7, St8, St9, St10, St12, St13, St14])
        db.session.commit()

        Rc1 = Receipt(created_date='2024-1-30 09:45:00', user_id=1, employee_id=3, flight_id=1,
                      quantity=3,
                      unit_price=3600000)
        Rc2 = Receipt(created_date='2024-1-30 19:15:00', user_id=2, employee_id=2, flight_id=1,
                      quantity=2,
                      unit_price=3000000)
        Rc3 = Receipt(created_date='2023-12-22 21:10:00', user_id=3, employee_id=3, flight_id=1,
                      quantity=2,
                      unit_price=3000000)

        Rc4 = Receipt(created_date='2023-12-30 09:45:00', user_id=4, employee_id=2, flight_id=2,
                      quantity=3,
                      unit_price=5100000)
        Rc5 = Receipt(created_date='2023-12-30 19:15:00', user_id=2, employee_id=2, flight_id=2,
                      quantity=2,
                      unit_price=4400000)
        Rc6 = Receipt(created_date='2023-12-22 21:10:00', user_id=7, employee_id=3, flight_id=2,
                      quantity=2,
                      unit_price=4400000)

        Rc7 = Receipt(created_date='2024-1-30 09:45:00', user_id=1, employee_id=2, flight_id=4,
                      quantity=3,
                      unit_price=5100000)
        Rc8 = Receipt(created_date='2024-1-30 19:15:00', user_id=5, employee_id=3, flight_id=4,
                      quantity=2,
                      unit_price=6400000)
        Rc9 = Receipt(created_date='2024-1-22 21:10:00', user_id=3, employee_id=2, flight_id=4,
                      quantity=2,
                      unit_price=6400000)

        Rc10 = Receipt(created_date='2023-12-30 09:45:00', user_id=1, employee_id=3, flight_id=6,
                       quantity=3,
                       unit_price=5100000)
        Rc11 = Receipt(created_date='2023-12-30 19:15:00', user_id=4, employee_id=3, flight_id=6,
                       quantity=2,
                       unit_price=4400000)
        Rc12 = Receipt(created_date='2023-12-22 21:10:00', user_id=6, employee_id=3, flight_id=6,
                       quantity=2,
                       unit_price=4400000)

        Rc13 = Receipt(created_date='2023-12-30 09:45:00', user_id=6, employee_id=3, flight_id=7,
                       quantity=3,
                       unit_price=4500000)
        Rc14 = Receipt(created_date='2023-12-30 19:15:00', user_id=1, employee_id=3, flight_id=7,
                       quantity=2,
                       unit_price=3600000)
        Rc15 = Receipt(created_date='2023-12-22 21:10:00', user_id=3, employee_id=3, flight_id=7,
                       quantity=2,
                       unit_price=3600000)
        db.session.add_all([Rc1, Rc2, Rc3, Rc4, Rc5, Rc6, Rc7, Rc8, Rc9, Rc10, Rc11, Rc12, Rc13, Rc14, Rc15])
        db.session.commit()

        Tp1 = TicketPrice(price=1200000, ticket_class_id=1, flight_id=1)
        Tp2 = TicketPrice(price=1500000, ticket_class_id=2, flight_id=1)

        Tp3 = TicketPrice(price=1700000, ticket_class_id=1, flight_id=2)
        Tp4 = TicketPrice(price=2200000, ticket_class_id=2, flight_id=2)

        Tp5 = TicketPrice(price=1900000, ticket_class_id=1, flight_id=3)
        Tp6 = TicketPrice(price=2500000, ticket_class_id=2, flight_id=3)

        Tp7 = TicketPrice(price=1700000, ticket_class_id=1, flight_id=4)
        Tp8 = TicketPrice(price=3200000, ticket_class_id=2, flight_id=4)

        Tp9 = TicketPrice(price=2500000, ticket_class_id=1, flight_id=5)
        Tp10 = TicketPrice(price=3500000, ticket_class_id=2, flight_id=5)

        Tp11 = TicketPrice(price=1700000, ticket_class_id=1, flight_id=6)
        Tp12 = TicketPrice(price=2200000, ticket_class_id=2, flight_id=6)

        Tp13 = TicketPrice(price=1500000, ticket_class_id=1, flight_id=7)
        Tp14 = TicketPrice(price=1800000, ticket_class_id=2, flight_id=7)

        Tp15 = TicketPrice(price=3500000, ticket_class_id=1, flight_id=8)
        Tp16 = TicketPrice(price=4000000, ticket_class_id=2, flight_id=8)

        db.session.add_all([Tp1, Tp2, Tp3, Tp4, Tp5, Tp6, Tp7, Tp8, Tp9, Tp10, Tp11,
                            Tp12, Tp13, Tp14, Tp15, Tp16])
        db.session.commit()

        T1 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, flight_id=1, customer_id=1, ticket_class_id=1)
        T2 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, flight_id=1, customer_id=2, ticket_class_id=1)
        T3 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, flight_id=1, customer_id=3, ticket_class_id=1)
        T4 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, flight_id=1, customer_id=4, ticket_class_id=2)
        T5 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, flight_id=1, customer_id=5, ticket_class_id=2)
        T6 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, flight_id=1, customer_id=6, ticket_class_id=2)
        T7 = Ticket(purchase_time='2023-12-31 03:0:00', seat_id=19, flight_id=1, customer_id=7, ticket_class_id=2)

        T8 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, flight_id=2, customer_id=1, ticket_class_id=1)
        T9 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, flight_id=2, customer_id=2, ticket_class_id=1)
        T10 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, flight_id=2, customer_id=3, ticket_class_id=1)
        T11 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, flight_id=2, customer_id=1, ticket_class_id=2)
        T12 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, flight_id=2, customer_id=5, ticket_class_id=2)
        T13 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, flight_id=2, customer_id=7, ticket_class_id=2)
        T14 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=19, flight_id=2, customer_id=6, ticket_class_id=2)

        T15 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, flight_id=4, customer_id=1, ticket_class_id=1)
        T16 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, flight_id=4, customer_id=2, ticket_class_id=1)
        T17 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, flight_id=4, customer_id=3, ticket_class_id=1)
        T18 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, flight_id=4, customer_id=1, ticket_class_id=2)
        T19 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, flight_id=4, customer_id=6, ticket_class_id=2)
        T20 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, flight_id=4, customer_id=1, ticket_class_id=2)
        T21 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=19, flight_id=4, customer_id=5, ticket_class_id=2)

        T22 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, flight_id=6, customer_id=3, ticket_class_id=1)
        T23 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, flight_id=6, customer_id=4, ticket_class_id=1)
        T24 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, flight_id=6, customer_id=6, ticket_class_id=1)
        T25 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, flight_id=6, customer_id=1, ticket_class_id=2)
        T26 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, flight_id=6, customer_id=2, ticket_class_id=2)
        T27 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, flight_id=6, customer_id=7, ticket_class_id=2)
        T28 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=19, flight_id=6, customer_id=1, ticket_class_id=2)

        T29 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=1, flight_id=7, customer_id=1, ticket_class_id=1)
        T30 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=2, flight_id=7, customer_id=2, ticket_class_id=1)
        T31 = Ticket(purchase_time='2023-12-31 02:00:00', seat_id=3, flight_id=7, customer_id=3, ticket_class_id=1)
        T32 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=16, flight_id=7, customer_id=6, ticket_class_id=2)
        T33 = Ticket(purchase_time='2023-12-31 01:00:00', seat_id=17, flight_id=7, customer_id=1, ticket_class_id=2)
        T34 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=18, flight_id=7, customer_id=5, ticket_class_id=2)
        T35 = Ticket(purchase_time='2023-12-31 03:00:00', seat_id=19, flight_id=7, customer_id=4, ticket_class_id=2)

        db.session.add_all([T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16,
                            T17, T18, T19, T20, T21, T22, T23, T24, T25, T26, T27, T28, T29, T30, T31, T32, T33, T34,
                            T35])
        db.session.commit()

        rcd1 = ReceiptDetail(ticket_id=1, receipt_id=1)
        rcd2 = ReceiptDetail(ticket_id=2, receipt_id=1)
        rcd3 = ReceiptDetail(ticket_id=3, receipt_id=1)
        rcd4 = ReceiptDetail(ticket_id=4, receipt_id=2)
        rcd5 = ReceiptDetail(ticket_id=5, receipt_id=2)
        rcd6 = ReceiptDetail(ticket_id=6, receipt_id=3)
        rcd7 = ReceiptDetail(ticket_id=7, receipt_id=3)
        db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        db.session.commit()

        rcd1 = ReceiptDetail(ticket_id=1, receipt_id=4)
        rcd2 = ReceiptDetail(ticket_id=2, receipt_id=4)
        rcd3 = ReceiptDetail(ticket_id=3, receipt_id=4)
        rcd4 = ReceiptDetail(ticket_id=4, receipt_id=5)
        rcd5 = ReceiptDetail(ticket_id=5, receipt_id=5)
        rcd6 = ReceiptDetail(ticket_id=6, receipt_id=6)
        rcd7 = ReceiptDetail(ticket_id=7, receipt_id=6)
        db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        db.session.commit()

        rcd1 = ReceiptDetail(ticket_id=1, receipt_id=7)
        rcd2 = ReceiptDetail(ticket_id=2, receipt_id=7)
        rcd3 = ReceiptDetail(ticket_id=3, receipt_id=7)
        rcd4 = ReceiptDetail(ticket_id=4, receipt_id=8)
        rcd5 = ReceiptDetail(ticket_id=5, receipt_id=8)
        rcd6 = ReceiptDetail(ticket_id=6, receipt_id=9)
        rcd7 = ReceiptDetail(ticket_id=7, receipt_id=9)
        db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        db.session.commit()

        rcd1 = ReceiptDetail(ticket_id=1, receipt_id=10)
        rcd2 = ReceiptDetail(ticket_id=2, receipt_id=10)
        rcd3 = ReceiptDetail(ticket_id=3, receipt_id=10)
        rcd4 = ReceiptDetail(ticket_id=4, receipt_id=11)
        rcd5 = ReceiptDetail(ticket_id=5, receipt_id=11)
        rcd6 = ReceiptDetail(ticket_id=6, receipt_id=12)
        rcd7 = ReceiptDetail(ticket_id=7, receipt_id=12)
        db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        db.session.commit()

        rcd1 = ReceiptDetail(ticket_id=1, receipt_id=13)
        rcd2 = ReceiptDetail(ticket_id=2, receipt_id=13)
        rcd3 = ReceiptDetail(ticket_id=3, receipt_id=13)
        rcd4 = ReceiptDetail(ticket_id=4, receipt_id=14)
        rcd5 = ReceiptDetail(ticket_id=5, receipt_id=14)
        rcd6 = ReceiptDetail(ticket_id=6, receipt_id=15)
        rcd7 = ReceiptDetail(ticket_id=7, receipt_id=15)

        db.session.add_all([rcd1, rcd2, rcd3, rcd4, rcd5, rcd6, rcd7])
        db.session.commit()

        Sc1 = Schedules(plane_id=1, flight_id=1)
        Sc2 = Schedules(plane_id=2, flight_id=2)
        Sc3 = Schedules(plane_id=1, flight_id=3)
        Sc4 = Schedules(plane_id=3, flight_id=4)
        Sc5 = Schedules(plane_id=2, flight_id=5)
        Sc6 = Schedules(plane_id=4, flight_id=6)
        Sc7 = Schedules(plane_id=5, flight_id=7)
        Sc8 = Schedules(plane_id=3, flight_id=8)

        db.session.add_all([Sc1, Sc2, Sc3, Sc4, Sc5, Sc6, Sc7, Sc8])
        db.session.commit()
