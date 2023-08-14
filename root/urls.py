from django.urls import path
from . import views

app_name = 'root'

urlpatterns = [
    path('',views.index,name='index'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    path('mydashboard/',views.mydashboard,name='mydashboard'),
    path("search_bus/", views.search_bus, name="search_bus"),
    path('tours/',views.tours,name='tours'),
    path('daily_tours/',views.daily_tours,name='daily_tours'),
    path('offer_tours/',views.offer_tours,name='offer_tours'),
    path('<int:id>/tour_details/',views.tour_details,name='tour_details'),
    path('<int:id>/booking_details/',views.booking_details,name='booking_details'),
    path('<int:id>/tour_booking_details/',views.tour_booking_details,name='tour_booking_details'),
    path('userside_report/',views.userside_report,name='userside_report')
]
