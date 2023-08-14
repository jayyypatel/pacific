from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('<int:sid>/<str:date>/book_seat/',views.book_seat,name='book_seat'),
    path('success/',views.success,name='success'),
    path('success_stours/',views.success_stours,name='success_stours'),
    path('<int:id>/pdf_busbooking/',views.pdf_busbooking,name='pdf_busbooking'),
    path('<int:id>/pdf_tourbooking/',views.pdf_tourbooking,name='pdf_tourbooking')
]