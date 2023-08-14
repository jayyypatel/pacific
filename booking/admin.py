from django.contrib import admin
from .models import Bus,BusBookings,BusBookings_details,Address,Routes,Schedules,Seat,Special_Tours,STourBooking_details,STourBooking
# Register your models here.

admin.site.register(Bus)
admin.site.register(BusBookings)
admin.site.register(BusBookings_details)
admin.site.register(Address)
admin.site.register(Routes)
admin.site.register(Schedules)
admin.site.register(Seat)
admin.site.register(Special_Tours)
admin.site.register(STourBooking)
admin.site.register(STourBooking_details)