from django.urls import path
from . import views

app_name = 'manager'


urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('<int:id>/del_contact_us/',views.del_contact_us, name="del_contact_us"),
    path('all_users',views.all_users,name='all_users'),
    path('bus_registration/',views.bus_registration,name='bus_registration'),
    path('add_bus_seat/',views.add_bus_seat,name='add_bus_seat'),
    path('<int:id>/del_bus/',views.del_bus, name="del_bus"),
    path('add_routes/',views.add_routes,name='add_routes'),
    path('add_address/',views.add_address,name='add_address'),
    path('add_schedules/',views.add_schedules,name='add_schedules'),
    path('add_special_tours/',views.add_special_tours,name='add_special_tours'),
    path('<int:id>/del_stours/',views.del_stours, name="del_stours"),
    path('<int:id>/stours_details/',views.stours_details, name="stours_details"),
    path('all_bookings/',views.all_bookings,name='all_bookings'),
    path('<int:sid>/<str:d>/ubb_details/',views.ubb_details,name='ubb_details'),
    path('tour_bookings/',views.tour_bookings,name='tour_bookings'),
    path('<int:id>/tb_details/',views.tb_details,name='tb_details'),
    path('top_5users/',views.top_5users,name='top_5users'),
    path('top_5destinations/',views.top_5destinations,name='top_5destinations'),
    path('all_users_report/',views.all_users_report,name='all_users_report'),
    path('top_tours_report/',views.top_tours_report,name='top_tours_report')
]
