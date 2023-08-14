from django.shortcuts import render,redirect
from .models import Schedules,Bus,Seat,BusBookings,BusBookings_details,STourBooking,STourBooking_details,Special_Tours
from auth_system.models import CustomUser
from django.utils import timezone
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta,datetime,time
#email
from django.conf import settings
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.template.loader import get_template,render_to_string
from django.contrib.auth.decorators import login_required
import socket
from .utils import send_email,send_email_manager
#pdf 
from weasyprint import HTML
import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='auth_system:login_user') 
def book_seat(request,sid,date):
    

    s_obj = Schedules.objects.get(id=sid)
    bus_s_obj = Bus.objects.get(id=s_obj.route_fk.bus_fk.id)

    date_only = date
    seat_booked = BusBookings_details.objects.filter(busbookings_fk__schedules_fk=s_obj,date=date_only,busbookings_fk__paid=True)#,date=date_only.strftime('%Y/%m/%d')
    s_list = [i.seat_fk.seat_name for i in seat_booked]
    seats = Seat.objects.exclude(seat_name__in=s_list)
    available_seats = Seat.objects.filter(bus_fk=bus_s_obj,id__in=seats)# i added here bus_fk=bus_s_obj,

    user_id = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':

        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        
        seats_list = request.POST.getlist('seats')
        

        t_price = len(seats_list) * int(s_obj.price)
        
        fname = first_name+' '+last_name

        BusBookings.objects.create(name=fname,total_price=str(t_price),user_fk=user_id,schedules_fk=s_obj,travel_date=date)
        busb_fk = BusBookings.objects.latest('id')

        for i in seats_list:
            seat = Seat.objects.get(seat_name=i)

            BusBookings_details.objects.create(busbookings_fk=busb_fk,seat_fk=seat,date=date)

        #for razorpay
        t_price= t_price*100
        client = razorpay.Client(auth=("rzp_test_susforIvG6nYky", "VUQ8dfvBSkVS9Lstz9r1pQ9r"))
        payment = client.order.create({'amount': t_price, 'currency': 'INR','payment_capture': '1'})

        busb_fk.razorpay_order_id = payment['id']
        busb_fk.save()
        return render(request, 'booking/razorpay.html', {'payment': payment})
    
    context ={
        'data':s_obj,
        'date':date,
        'seats':available_seats,
        's_count':available_seats.count()
        
    }
    return render(request,'root/book_seat.html',context)


@csrf_exempt
def success(request):
    flag = ''
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        flag='net_on'
    except OSError:
        flag='net_off'

    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        book = BusBookings.objects.filter(razorpay_order_id = order_id).first()
        book.paid = True
        book.save()

        l_user = CustomUser.objects.get(pk=request.user.id)
        subject1 = "Your Seat Is Booked  - Pacific"
        msg = f'Your Seat has been Booked and Razorpay payment id is : {order_id}'
        to_mail1 = l_user.email
        tmp = 'booking/email_seatBook_successful.html'
        
        #this mail will go to user 
        #from utils.py user defined function 
        send_email(subject=subject1,to_mail=to_mail1,message=msg,tmp_url=tmp)

        #this mail will go to manager 
        subject1 = "Seat Booked - Pacific"
        msg = f'Seat Booked by {book.name} from: {book.schedules_fk}'
        to_mail1 = 'settings.EMAIL_HOST_USER'
        tmp = 'booking/email_seatBook_manager.html'
        n=book.name
        send_email_manager(subject=subject1,message=msg,tmp_url=tmp,name=n)

        #admin side email send kravo

    return render(request, "booking/success.html")

@csrf_exempt
def success_stours(request):
    flag = ''
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        flag='net_on'
    except OSError:
        flag='net_off'

    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        book = STourBooking.objects.filter(razorpay_order_id = order_id).first()
        book.paid = True
        book.save()

        l_user = CustomUser.objects.get(pk=request.user.id)
        subject1 = "Your Seat Is Booked For Tour- Pacific"
        msg = f'Your Seat has been Booked for Tour: {book.special_tours_fk.name} and Razorpay payment id is : {order_id}'
        to_mail1 = l_user.email
        tmp = 'booking/email_seatBook_successful.html'
        
        #this mail will go to user 
        #from utils.py user defined function created for own purpose
        send_email(subject=subject1,to_mail=to_mail1,message=msg,tmp_url=tmp)

        #this mail will go to manager 
        subject1 = "Seat Booked For Tour- Pacific"
        msg = f'Seat Booked by {book.name} for: {book.special_tours_fk.name}'
        to_mail1 = 'settings.EMAIL_HOST_USER'
        tmp = 'booking/email_seatBook_manager.html'
        n=book.name
        send_email_manager(subject=subject1,message=msg,tmp_url=tmp,name=n)

        #admin side email send kravo

    return render(request, "booking/success.html")

download_path = os.path.join(settings.MEDIA_ROOT,'invoice.pdf')
def pdf_busbooking(request,id):

    data_booking = BusBookings.objects.get(id=id)
    seats = BusBookings_details.objects.filter(busbookings_fk=data_booking)

    context = {
        'data':data_booking,
        'seats':seats,
        's_cnt':seats.count()
    }    

    template_render  = render_to_string('booking/invoice.html', context)
    html = HTML(string=template_render)
    html.write_pdf(target=download_path)

    fs = FileSystemStorage(settings.MEDIA_ROOT)
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    return response

download_path = os.path.join(settings.MEDIA_ROOT,'invoice.pdf')
def pdf_tourbooking(request,id):
    dis = ''
    data_booking = STourBooking.objects.get(id=id)
    tour = Special_Tours.objects.get(id=data_booking.special_tours_fk.id)
    seats = STourBooking_details.objects.filter(stourbooking_fk=data_booking)
    if tour.offer:
        dis = tour.price * 10 / 100
    context = {
        'data':data_booking,
        'seats':seats,
        's_cnt':seats.count(),
        'dis':dis
    }    

    template_render  = render_to_string('booking/invoice_tours.html', context)
    html = HTML(string=template_render)
    html.write_pdf(target=download_path)

    fs = FileSystemStorage(settings.MEDIA_ROOT)
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    return response