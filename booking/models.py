from django.db import models
from auth_system.models import CustomUser
from django.utils import timezone

class Address(models.Model):
    city = models.CharField(max_length=100,blank=False,null=False,unique=True)
    state = models.CharField(max_length=100,blank=False,null=False)
    pincode = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return f'{self.id} {self.city}'

t_type = (
    ('ac','AC'),
    ('non-ac','Non-AC')
)
s_type = (
    ('ac-seat(2+1)','AC Seat(2+1)'),
    ('non-ac-seat(2+2)','Non-AC Seat(2+2)'),
    ('ac-sleeper(2+1)','AC Sleeper(2+1)'),
    ('non-ac-sleeper(2+1)','Non-AC Sleeper(2+1)')
)

class Bus(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    driver_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    plate_no = models.CharField(max_length=50)
    check_ac = models.CharField(max_length=10,choices=t_type,default='non-ac') 
    seat_type = models.CharField(max_length=25,choices=s_type,default='non-ac-seat(2+2)')  # new on 28-1
    max_seats = models.IntegerField()

    def __str__(self):
        return f'id: {self.id} {self.name} {self.seat_type}'



class Routes(models.Model):
    bus_fk = models.ForeignKey(Bus,on_delete=models.CASCADE,related_name='routes_bus')
    origin_fk = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='routes_origin_address')
    destination_fk = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='routes_destination_address')
    # insert data in stops_city like 'ahm to surat= baroda, ankleshvar,' so we can extract with ','
    stops_city = models.CharField(max_length=100,default='')
    distance = models.CharField(max_length=255,null=False,blank=False)
    boarding_point = models.CharField(max_length=50,null=True,blank=True)
    dropping_point = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return f'Rid: {self.id} , {self.origin_fk} , {self.destination_fk} , {self.bus_fk}'



class Schedules(models.Model):
    route_fk = models.ForeignKey(Routes,on_delete=models.CASCADE,related_name='schedules_route')
    departureTime = models.TimeField()
    arrivalTime = models.TimeField()
    duration = models.CharField(max_length=20)
    price = models.CharField(max_length=20)

    # insert data in daysOfWeek like 'sunday, monday, tuesday, friday,' so we can extract with ','
    daysOfWeek = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return f'{self.id} {self.route_fk}'

class Seat(models.Model):          
    status = models.BooleanField(default=False)    
    date = models.DateField(default=timezone.now,blank=True,null=True)
    time = models.TimeField(default=timezone.now,blank=True,null=True)
    
    seat_name = models.CharField(max_length=10,blank=False,null=False,unique=True)
    bus_fk = models.ForeignKey(Bus,on_delete=models.CASCADE,related_name='seat_bus')
    
    def __str__(self):
        return f'{self.seat_name} B:- {self.bus_fk}'

class BusBookings(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    total_price = models.IntegerField()
    user_fk = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='busbookings_user')
    schedules_fk = models.ForeignKey(Schedules,on_delete=models.CASCADE,related_name='busbookings_schedules')
    #
    travel_date = models.DateField(default=timezone.now)
    #a both date current
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    #for razorpay
    razorpay_order_id = models.CharField(max_length=1000,blank=True,null=True)
    paid = models.BooleanField(default=False,blank=True,null=True)
    confirm = models.BooleanField(default=False,blank=True,null=True)


class BusBookings_details(models.Model):#book_details tbl
    busbookings_fk = models.ForeignKey(BusBookings,on_delete=models.CASCADE,related_name='book_details_busbooking')
    # seat_number = models.IntegerField()
    seat_fk = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name='busbooking_details_seat_fk')
    #this date is for bus travel date
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)


class Special_Tours(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    bus_fk_k = models.ForeignKey(Bus,on_delete=models.CASCADE,related_name='special_tours_bus')
    description = models.CharField(max_length=1000)
    schedule = models.CharField(max_length=2000)
    origin_fk_k = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='special_tours_origin_address')
    destination_fk_k = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='special_tours_destination_address')
    price = models.IntegerField()
    total_days = models.CharField(max_length=15)
    boarding_point = models.CharField(max_length=50,null=True,blank=True)
    dropping_point = models.CharField(max_length=50,null=True,blank=True)
    offer = models.BooleanField(default=False,blank=True,null=True)
    offer_per = models.CharField(max_length=10,default='',null=True,blank=True)
    img1 = models.ImageField(upload_to='Images',blank=True,null=True)
    img2 = models.ImageField(upload_to='Images',blank=True,null=True)
    img3 = models.ImageField(upload_to='Images',blank=True,null=True)
    img4 = models.ImageField(upload_to='Images',blank=True,null=True)
    
    def _str_(self):
        return f'{self.name}'

    def get_img1_url(self):
        return self.img1.url

    def get_img2_url(self):
        return self.img2.url

    def get_img3_url(self):
        return self.img3.url
    
    def get_img4_url(self):
        return self.img4.url

class STourBooking(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    total_price = models.IntegerField()
    user_fk = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='stour_booking_user')
    special_tours_fk = models.ForeignKey(Special_Tours,on_delete=models.CASCADE,related_name='stour_booking_Special_Tours')
    travel_date = models.DateField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    #for razorpay
    razorpay_order_id = models.CharField(max_length=1000,blank=True,null=True)
    paid = models.BooleanField(default=False,blank=True,null=True)
    confirm = models.BooleanField(default=False,blank=True,null=True)

class STourBooking_details(models.Model):
    stourbooking_fk = models.ForeignKey(STourBooking,on_delete=models.CASCADE,related_name='stourbooking_details_STourBooking')
    # seat_number = models.IntegerField()
    seat_fk = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name='stourbooking_details_seat_fk')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)




