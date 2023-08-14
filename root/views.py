from django.shortcuts import render,redirect
from .forms import EmailForm
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPAuthenticationError,SMTPException
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template,render_to_string
from .forms import search_busForm
from booking.models import Routes,Schedules,Special_Tours
from datetime import datetime
import socket
from booking.models import BusBookings,BusBookings_details,Seat,STourBooking,STourBooking_details
from auth_system.models import CustomUser
import razorpay
# Create your views here.
def index(request):

    tours_Data = Special_Tours.objects.filter(start_date__gte=datetime.now()).order_by('-id')

    context = {
        'form':search_busForm(),
        'tours_Data':tours_Data
    }
    return render(request,'root/index.html',context)

def search_bus(request):
    if request.method == 'POST':
        from_d = request.POST['from_d']
        to_d = request.POST['to_d']
        date_d = request.POST['date']

        date_obj = datetime.strptime(date_d, '%Y-%m-%d')
        day_date_obj = date_obj.strftime('%A')
        print(day_date_obj) # 2023-01-29
        #comments
        if not from_d :
            return redirect('root:index')
        else:

            lookups = Q(route_fk__origin_fk__city__icontains=from_d) & Q(route_fk__destination_fk__city__icontains=to_d) & Q(daysOfWeek__icontains=day_date_obj) 

            results = Schedules.objects.filter(lookups).distinct()
            
            if results.exists():

                context = {
                            'results': results,
                            'r_count': results.count(),
                            'date': date_d
                        }
                return render(request, 'root/search_bus.html', context)
            else:

                return render(request, 'root/search_not_found.html', {'from_d': from_d,'to_d':from_d})

    
    context = {
        
    }
    return render(request,'root/search_bus.html',context)
    

def contact_us(request):
    form = EmailForm()
    
    flag = ''
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        flag='net_on'
    except OSError:
        flag='net_off'

    if request.method == 'POST':
        form = EmailForm(request.POST)
        
        if form.is_valid():
            to_mail = form.cleaned_data.get('email_id')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            form.save()
            
            #reply as email to contected person
            e_tmp = 'root/email_thank_contactus.html'
            c = {'name':request.POST['name']}
            content = render_to_string(e_tmp,c)
            img_data = open('static/email_img/logo_2.png', 'rb').read()
            html_part = MIMEMultipart(_subtype='related')
            body = MIMEText(content, _subtype='html')
            html_part.attach(body)
            # Now create the MIME container for the image
            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>')  # angle brackets are important
            img_data2 = open('static/email_img/logo_small.jpg', 'rb').read()
            img2 = MIMEImage(img_data2, 'jpg')
            img2.add_header('Content-Id', '<myimage2>')  # angle brackets are important
            # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
            html_part.attach(img)
            html_part.attach(img2)
            msg = EmailMessage("Contact Us request received", None,  settings.EMAIL_HOST_USER,  [to_mail])
            msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
            if flag == 'net_on':
                msg.send()
            else:
                print('network is not on')


            #?msg send to admin or manager's email id 
            e_tmp = 'root/email_received_contact.html'
            c = {
                'name':request.POST['name'],
                'msg':request.POST['message']
            }
            content = render_to_string(e_tmp,c)
            img_data = open('static/email_img/logo_2.png', 'rb').read()
            html_part = MIMEMultipart(_subtype='related')
            body = MIMEText(content, _subtype='html')
            html_part.attach(body)
            # Now create the MIME container for the image
            img = MIMEImage(img_data, 'png')
            img.add_header('Content-Id', '<myimage>')  # angle brackets are important
            img_data2 = open('static/email_img/logo_small.jpg', 'rb').read()
            img2 = MIMEImage(img_data2, 'jpg')
            img2.add_header('Content-Id', '<myimage2>')  # angle brackets are important
            # img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
            html_part.attach(img)
            html_part.attach(img2)
            msg = EmailMessage("Contact Us request received", None,  settings.EMAIL_HOST_USER,  [settings.EMAIL_HOST_USER])
            msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
            if flag == 'net_on':
                msg.send()
            else:
                print('network is not on')
            
            return redirect('root:contact_us')
            
    context ={
        'form':form
    }
    return render(request,'root/contactus.html',context)


def about_us(request): 
    context = { 

    }
    return render(request,'root/about_us.html',context)


@login_required(login_url='auth_system:login_user') 
def mydashboard(request):
    current_date = datetime.now()
    user = CustomUser.objects.get(id=request.user.id)
    future_seat_booking = BusBookings.objects.filter(user_fk=user,travel_date__gte=current_date,paid=True)#,date__gte=current_date

    future_tour_bookings = STourBooking.objects.filter(user_fk=user,travel_date__gte=current_date,paid=True)

    context = {
        'up_seat_booking':future_seat_booking,
        'up_tour_booking':future_tour_bookings
    }
    return render(request,'root/mydashboard.html',context)


def tours(request):

    context = {
        'data':Special_Tours.objects.filter(start_date__gte=datetime.now())
    }
    return render(request,'root/tours.html',context)

def daily_tours(request):
    

    d = datetime.date(datetime.now())
    date_obj = datetime.strptime(str(d), '%Y-%m-%d')
    day_date_obj = date_obj.strftime('%A')
    print(day_date_obj)

    data = Schedules.objects.filter(daysOfWeek__icontains = day_date_obj)#
    context = {
        'results':data,
        'date':date_obj.strftime('%Y-%m-%d'),
        
    }
    return render(request,'root/daily_tour.html',context)

def offer_tours(request):
    context = {
        'data':Special_Tours.objects.filter(start_date__gte=datetime.now(),offer=True)
    }
    return render(request,'root/tours.html',context)

@login_required(login_url='auth_system:login_user')
def tour_details(request,id):
    data = Special_Tours.objects.get(id=id)
    
    
    seat_booked = STourBooking_details.objects.filter(stourbooking_fk__paid=True,stourbooking_fk__special_tours_fk=data)#,date=date_only.strftime('%Y/%m/%d')
    s_list = [i.seat_fk.seat_name for i in seat_booked]
    seats = Seat.objects.exclude(seat_name__in=s_list)
    available_seats = Seat.objects.filter(bus_fk=data.bus_fk_k,id__in=seats)

    user_id = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':

        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        seat_list = request.POST.getlist('seats')

        t_price = len(seat_list) * int(data.price)
        if data.offer:
            minus = (t_price * 10) / 100
            t_price = t_price - int(minus)
        fname = first_name+' '+last_name

        STourBooking.objects.create(name=fname,total_price=t_price,user_fk=user_id,special_tours_fk=data,travel_date=data.start_date,)
        Latest_STourB = STourBooking.objects.latest('id')

        for i in seat_list:
            seat = Seat.objects.get(seat_name=i)

            STourBooking_details.objects.create(stourbooking_fk=Latest_STourB,seat_fk=seat,date=datetime.now())

        t_price= t_price*100
        client = razorpay.Client(auth=("rzp_test_susforIvG6nYky", "VUQ8dfvBSkVS9Lstz9r1pQ9r"))
        payment = client.order.create({'amount': t_price, 'currency': 'INR','payment_capture': '1'})

        Latest_STourB.razorpay_order_id = payment['id']
        Latest_STourB.save()
        return render(request, 'booking/razorpay_stours.html', {'payment': payment})


    context = {
        'data': data,
        'seats':available_seats
    }
    return render(request,'root/tour_details.html',context)

@login_required(login_url='auth_system:login_user')
def booking_details(request,id):
    data = BusBookings.objects.get(id=id)
    seats = BusBookings_details.objects.filter(busbookings_fk=data)
    cnt = seats.count()
    context={
        'data':data,
        'seats':seats,
        's_cnt':cnt
    }
    return render(request,'root/booking_details.html',context)

@login_required(login_url='auth_system:login_user')
def tour_booking_details(request,id):
    dis = ''
    data = STourBooking.objects.get(id=id)
    tour = Special_Tours.objects.get(id=data.special_tours_fk.id)
    seats = STourBooking_details.objects.filter(stourbooking_fk=data)
    cnt = seats.count()
    if tour.offer:
        dis = tour.price * 10 / 100
    context={
        'data':data,
        'seats':seats,
        's_cnt':cnt,
        'dis':dis
    }
    return render(request,'root/tour_booking_details.html',context)

def userside_report(request):

    return render(request,'root/userside_report.html')