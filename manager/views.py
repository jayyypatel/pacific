from django.shortcuts import render,redirect
from root.models import Mailbox
from django.contrib.auth.decorators import login_required
from auth_system.models import CustomUser
from booking.forms import Bus_registrationForm,Add_RoutesForm,Add_addressForm,Add_schedulesForm,add_bus_seatForm,Add_Special_toursForm
from django.contrib import messages
from booking.models import Bus,Address,Routes,Schedules,Seat,Special_Tours,BusBookings,BusBookings_details,STourBooking,STourBooking_details
from django.db.models import Count
from datetime import datetime
from .utils import pdf
from django.db.models import Avg, Max, Min
from django.db.models import OuterRef, Subquery
# Create your views here.
@login_required(login_url='auth_system:login_user') 
def dashboard(request):
    bus_count = Bus.objects.all().count()
    route_count = Routes.objects.all().count()
    schedules_count = Schedules.objects.all().count()
    users_count = CustomUser.objects.all().count()
    contact_count = Mailbox.objects.all().count()
    st_count = Special_Tours.objects.all().count()
    context={
        'bus_count':bus_count,
        'route_count':route_count,
        'schedules_count':schedules_count,
        'users_count':users_count - 2,
        'contact_count':contact_count,
        'st_count':st_count
    }
    return render(request,'manager/index.html',context)


@login_required(login_url='auth_system:login_user')  
def contact_us(request):
    data = Mailbox.objects.all()
    context = {
        'data':data
    }
    return render(request,'manager/contactus.html',context)

@login_required(login_url='auth_system:login_user') 
def del_contact_us(request,id):
    contact = Mailbox.objects.get(id=id)
    contact.delete()
    return redirect('manager:contact_us')

@login_required(login_url='auth_system:login_user') 
def all_users(request):
    users = CustomUser.objects.filter(user_type = 'customer')
    cnt = CustomUser.objects.all().count() - 2 # 1 for admin and 1 for manager 
    context = {
        'data':users,
        'cnt':cnt
    }
    return render(request,'manager/all_users.html',context)

@login_required(login_url='auth_system:login_user') 
def bus_registration(request):
    if request.method == 'POST':
        
        form = Bus_registrationForm(request.POST,request.FILES)   
        
        if form.is_valid():
            form.save()
            messages.success(request,'Bus added successfully.')
            return redirect('manager:bus_registration')
    else:
        form = Bus_registrationForm()

    context={
        'form':form,
        'cnt':Bus.objects.all().count(),
        'data':Bus.objects.all(),
        's_data':Seat.objects.all()
    } 
    return render(request,'manager/bus_registration.html',context)

@login_required(login_url='auth_system:login_user') 
def add_bus_seat(request):
    if request.method == 'POST':
        
        form = add_bus_seatForm(request.POST)   
        
        if form.is_valid():
            # print(request.POST['seat_name'])
            b = Bus.objects.get(pk=request.POST['bus_fk'])
            if Seat.objects.filter(bus_fk= request.POST['bus_fk']).exists():
                messages.success(request,f'Seats of Bus : {b} already exists.')
                return redirect('manager:add_bus_seat')

            else:
                if int(request.POST['seat_count']) > b.max_seats:
                    messages.success(request,f'Bus : {b} Seat count Out of Max seats count.')
                    return redirect('manager:add_bus_seat')
                    
                else:
                    seat_cnt = request.POST['seat_count']
                    for i in range(1,int(seat_cnt)+1):
                        s_name = request.POST['seat_name'] + str(i) # S+1 = S1
                        
                        b_fk = Bus.objects.get(pk=request.POST['bus_fk'])
                        Seat.objects.create(seat_name=s_name,bus_fk=b_fk)

            
            messages.success(request,'All Seats added successfully.')
            return redirect('manager:add_bus_seat')
    else:
        form = add_bus_seatForm()

    context = {
        'form':form,
    }
    return render(request,'manager/add_bus_seat.html',context)

@login_required(login_url='auth_system:login_user') 
def del_bus(request,id):
    bus_obj = Bus.objects.get(id=id)
    bus_obj.delete()
    return redirect('manager:bus_registration')

@login_required(login_url='auth_system:login_user') 
def add_routes(request):
    if request.method == 'POST':
        
        form = Add_RoutesForm(request.POST,request.FILES)   
        
        if form.is_valid():
            # print(request.POST['origin_fk'])
            if request.POST['origin_fk'] == request.POST['destination_fk']:
                messages.success(request,'Please do not select same city as origin and distanation.')
                return redirect('manager:add_routes')
            else:
                form.save()
                messages.success(request,'Route added successfully.')
                return redirect('manager:add_routes')
    else:
        form = Add_RoutesForm()
    context={
        'form':form,
        'cnt':Routes.objects.all().count(),
        'data':Routes.objects.all()
    } 
    return render(request,'manager/add_routes.html',context)

@login_required(login_url='auth_system:login_user') 
def add_address(request):
    if request.method == 'POST':
        
        form = Add_addressForm(request.POST,request.FILES)   
        
        if form.is_valid():
            # print(request.POST['origin_fk'])
            form.save()
            messages.success(request,'Address added successfully.')
            return redirect('manager:add_address')
    else:
        form = Add_addressForm()

    context={
        'form':form,
        'cnt':Address.objects.all().count(),
        'data':Address.objects.all()
    } 
    return render(request,'manager/add_address.html',context)

@login_required(login_url='auth_system:login_user') 
def add_schedules(request):
    if request.method == 'POST':
        
        form = Add_schedulesForm(request.POST,request.FILES)   
        
        if form.is_valid():
            # print(request.POST['origin_fk'])
            form.save()
            messages.success(request,'Schedule added successfully.')
            return redirect('manager:add_schedules')
    else:
        form = Add_schedulesForm()
    # d = Schedules.objects.get(id=1)
    # days = d.daysOfWeek
    # j = days.split(',')
    # for i in j:
    #     print(i.replace(' ',''))
    context={
        'form':form,
        'cnt':Schedules.objects.all().count(),
        'data':Schedules.objects.all()
    } 
    return render(request,'manager/add_shedules.html',context)


@login_required(login_url='auth_system:login_user') 
def add_special_tours(request):
    if request.method == 'POST':
        
        form = Add_Special_toursForm(request.POST,request.FILES)   
        
        if form.is_valid():
            print("hello")
            form.save()
            messages.success(request,'Tour added successfully.')
            return redirect('manager:add_special_tours')
    else:
        form = Add_Special_toursForm()

    context={
        'form':form,
        'cnt':Special_Tours.objects.all().count(),
        'data':Special_Tours.objects.all(), 
    }
    return render(request,'manager/add_special_tours.html',context)

@login_required(login_url='auth_system:login_user') 
def del_stours(request,id):
    bus_obj = Special_Tours.objects.get(id=id)
    bus_obj.delete()

    return redirect('manager:add_special_tours')

@login_required(login_url='auth_system:login_user') 
def stours_details(request,id):
    sd_obj = Special_Tours.objects.get(id=id)
    

    context={
        'data':sd_obj
    }
    
    return render(request,'manager/stours_details.html',context)


@login_required(login_url='auth_system:login_user') 
def all_bookings(request):
    current_date = datetime.now()
    #MyModel.objects.values('schedule_fk', 'travel_date').annotate(total=Count('id')).filter(total=1)
    #t = BusBookings.objects.filter(id__in=BusBookings.objects.values('schedules_fk', 'travel_date').annotate(min_id=Min('id')).values('min_id'))
    
    t = BusBookings.objects.filter(id=Subquery(
        BusBookings.objects.filter(
            schedules_fk=OuterRef('schedules_fk'),
            travel_date=OuterRef('travel_date'),travel_date__gte=current_date
        ).order_by('id').values('id')[:1]
    )).order_by('travel_date')


    #,id__in=distinct_data.keys()
    #! main
    #! data = BusBookings.objects.filter(travel_date__gte=current_date).values('id','schedules_fk','schedules_fk__route_fk__bus_fk__plate_no','total_price','schedules_fk__route_fk__origin_fk__city','schedules_fk__route_fk__destination_fk__city','travel_date').annotate(bcnt=Count('schedules_fk')).order_by('travel_date')
    #! main end
    
    # total_seat_cnt = BusBookings_details.objects.filter(busbookings_fk__in=list1).values('busbookings_fk','busbookings_fk__schedules_fk__route_fk__bus_fk__max_seats').annotate(cnt=Count('busbookings_fk')).order_by()
    
    
    # print()
    # print(total_seat_cnt)
    # print(data)
    # print()
    context={
        'data':t,
        # 'data_seat':total_seat_cnt
    }
    
    return render(request,'manager/all_bookings.html',context)

@login_required(login_url='auth_system:login_user') 
def ubb_details(request,sid,d):
    #b_data = BusBookings.objects.get(id=id)
    b_data = BusBookings.objects.filter(schedules_fk=sid)[:1]
    obj = BusBookings_details.objects.filter(busbookings_fk__paid=True,busbookings_fk__schedules_fk=sid,busbookings_fk__travel_date=d)

    tmp_dict = {}
    for i in b_data:
        tmp_dict['travel_date'] = d
        tmp_dict['b_num'] = i.schedules_fk.route_fk.bus_fk.plate_no
        tmp_dict['max_seat'] =i.schedules_fk.route_fk.bus_fk.max_seats
        tmp_dict['price'] = i.schedules_fk.price
        tmp_dict['dt'] = i.schedules_fk.departureTime
        tmp_dict['bp'] = i.schedules_fk.route_fk.boarding_point
        tmp_dict['at'] = i.schedules_fk.arrivalTime
        tmp_dict['dp'] = i.schedules_fk.route_fk.dropping_point
        tmp_dict['from'] = i.schedules_fk.route_fk.origin_fk.city
        tmp_dict['to'] = i.schedules_fk.route_fk.destination_fk.city

    context={
        'data':obj,
        'cnt':obj.count(),    
        'b_data':tmp_dict    
    }
    
    return render(request,'manager/ubb_details.html',context)

@login_required(login_url='auth_system:login_user')
def tour_bookings(request):
    up_tour_booking = STourBooking.objects.filter(paid=True,travel_date__gte=datetime.now())
    previous_tour_booking = STourBooking.objects.filter(paid=True,travel_date__lt=datetime.now())
    context = {
        'up_tour_booking':up_tour_booking,
        'previous_tour_booking':previous_tour_booking
    }
    return render(request,'manager/tour_bookings.html',context)

@login_required(login_url='auth_system:login_user') 
def tb_details(request,id):
    s_data = STourBooking.objects.get(id=id)
    obj = STourBooking_details.objects.filter(stourbooking_fk__paid=True,stourbooking_fk=s_data)
    

    context={
        'data':obj,
        'cnt':obj.count(),  
        's_data':s_data     
    }
    
    return render(request,'manager/tb_details.html',context)


def top_5users(request):

    today = datetime.now()
    top_five_customers = BusBookings.objects.filter().values('user_fk__username','user_fk__email').annotate(booking_count=Count('user_fk__username')).order_by('-booking_count',)[:5]
    msg = 'Top 5 Customers based on bookings '

    context={
                'top_5':top_five_customers,
                'date':today,
                'msg':msg,
                # 'rest':rest,
    }
    
    return pdf(context,'manager/top_users_report.html')

def top_5destinations(request):
    today = datetime.now()
    top_five_od = BusBookings.objects.filter().values('schedules_fk__route_fk__destination_fk__city','schedules_fk__route_fk__origin_fk__city').annotate(booking_count=Count('schedules_fk__route_fk')).order_by('-booking_count',)[:5]
    msg = 'Top 5 Origins and Destinations based on bookings '

    context={
                'top_5':top_five_od,
                'date':today,
                'msg':msg,
                # 'rest':rest,
    }

    # return redirect('manager:dashboard')
    return pdf(context,'manager/top_5destinations.html')

def top_tours_report(request):
    today = datetime.now()
    top_tours = STourBooking.objects.filter().values('special_tours_fk__name','special_tours_fk__price').annotate(booking_count=Count('special_tours_fk__id')).order_by('-booking_count',)[:5]
    msg = 'Top 5 Special Tours based on bookings '

    context={
                'top_5':top_tours,
                'date':today,
                'msg':msg,
                # 'rest':rest,
    }

    return pdf(context,'manager/top_tours_report.html')

def all_users_report(request):
    today = datetime.now()
    data = CustomUser.objects.exclude(username__in=['admin','manager'])
    msg = 'All Users on our site'

    context={
                'data':data,
                'date':today,
                'msg':msg,
                'cnt':data.count()
    }
   
    # return redirect('manager:dashboard')
    return pdf(context,'manager/all_users_report.html')
