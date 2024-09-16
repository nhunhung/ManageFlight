from ManageFlightApp.models import *
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin, BaseView
from ManageFlightApp import admin, db, utils
from flask import redirect, request


class AuthenticatedView(ModelView):
    column_display_pk = True
    create_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.ADMIN)


class FlightView(AuthenticatedView):
    column_filters = ["departure_time", "arrival_time"]


class CustomerView(AuthenticatedView):
    column_filters = ["username"]


class SeatView(AuthenticatedView):
    column_filters = ["number_seat"]
    column_list = ["number_seat", "status", "plane_id", "ticket_class_id"]


class TicketClassView(AuthenticatedView):
    column_filters = ["name"]


class TicketView(AuthenticatedView):
    column_filters = ["id"]


class PlaneView(AuthenticatedView):
    column_filters = ["name"]


class ReceiptView(AuthenticatedView):
    column_searchable_list = ["created_date", "id"]


class ReceiptDetailView(AuthenticatedView):
    column_searchable_list = ["id"]


class SchedulesView(AuthenticatedView):
    column_searchable_list = ["id"]


class RouteView(AuthenticatedView):
    column_filters = ["name"]


class AirportView(AuthenticatedView):
    column_filters = ["location"]


class TicketPriceView(AuthenticatedView):
    column_filters = ["id"]


class StopView(AuthenticatedView):
    column_filters = ["id"]


class AirlineView(AuthenticatedView):
    column_filters = ["id"]


class KindView(AuthenticatedView):
    column_filters = ["id"]


class EmployeeView(AuthenticatedView):
    column_filters = ["id"]


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/Manage.html', FlightStates=utils.flight_states())
        month = request.args.get("month", datetime.now())
        return self.render('admin/Manage.html', general_states=utils.General_States(m=month))


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.ADMIN)


class RevenueView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/RevenueStates.html', revenue_states=utils.revenue_states())


class FlightStatesView(BaseView):
    @expose("/")
    def index(self):
        # kw = request.args.get("kw")
        # year = request.args.get("year", datetime.now())
        return self.render('admin/FlightStates.html', FlightStates=utils.flight_states())

class PercentView(BaseView):
    @expose("/")
    def index(self):
        # kw = request.args.get("kw")
        # year = request.args.get("year", datetime.now())
        return self.render('admin/PercentStates.html', percent_states=utils.percent_states())


admin = Admin(app=app, name="QUẢN TRỊ ADMIN", template_mode="bootstrap4", index_view=MyAdminIndexView())

admin.add_view(CustomerView(Customer, db.session, category="Person"))
admin.add_view(EmployeeView(Employee, db.session, category="Person"))
admin.add_view(SeatView(Seat, db.session, category="Manage Ticket"))
admin.add_view(TicketView(Ticket, db.session, category="Manage Ticket"))
admin.add_view(TicketPriceView(TicketPrice, db.session, category="Manage Ticket"))
admin.add_view(TicketClassView(TicketClass, db.session, category="Manage Ticket"))
admin.add_view(ReceiptView(Receipt, db.session, category="Bill"))
admin.add_view(ReceiptDetailView(ReceiptDetail, db.session, category="Bill"))
admin.add_view(SchedulesView(Schedules, db.session, category="Manage chedules"))
admin.add_view(StopView(Stop, db.session, category="Manage chedules"))
admin.add_view(RouteView(Route, db.session, category="Manage Flight"))
admin.add_view(FlightView(Flight, db.session, category="Manage Flight"))
admin.add_view(AirportView(Airport, db.session, category="Manage Flight"))
admin.add_view(FlightStatesView(name="FlightStates", category="States"))
admin.add_view(PercentView(name="PercentStates", category="States"))
admin.add_view(RevenueView(name="RevenueStates", category="States"))
admin.add_view(LogoutView(name="Đăng xuất"))
