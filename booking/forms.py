from django import forms
from datetime import datetime
from .models import Bus,Routes,Address,Schedules,Special_Tours

class Bus_registrationForm(forms.ModelForm):
        class Meta:
                model = Bus
                fields = ['name','driver_name','contact','plate_no','seat_type','max_seats']
                widgets={
                        'name':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Fullname'}),
                        'driver_name':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Driver name'}),
                        'contact':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Contact Number'}),
                        'plate_no':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Plate no'}),
                        'seat_type':forms.Select(attrs={'class':'form-select','type':'input','placeholder':'Enter Plate no'}),
                        
                        'max_seats':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Maximum Seats'}) 
                }

class Add_RoutesForm(forms.ModelForm):
        class Meta:
                model = Routes
                fields = ['bus_fk','origin_fk','destination_fk','stops_city','distance','boarding_point','dropping_point']
                widgets={
                        'bus_fk':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'origin_fk':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'destination_fk':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'stops_city':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter all stops'}),
                        'distance':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Distance'}),
                        'boarding_point':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Boarding Point'}),
                        'dropping_point':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Dropping Point'})

                }

class Add_addressForm(forms.ModelForm):
        class Meta:
                model = Address
                fields = ['city','state','pincode']
                widgets = {
                        'city':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter City name'}),
                        'state':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter State name'}),
                        'pincode':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Pincode'}),
                }

class Add_schedulesForm(forms.ModelForm):
        class Meta:
                model = Schedules
                fields = ['route_fk','departureTime','arrivalTime','daysOfWeek','duration','price']
                widgets = {
                        'route_fk':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'departureTime' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'time'}),
                        'arrivalTime' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'time'}),
                        'daysOfWeek' : forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter like "sunday, monday, tuesday,"'}),
                        'duration':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Duration'}),
                        'price':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Price for ticket'})
                }

class add_bus_seatForm(forms.Form):
        seat_name = forms.CharField(max_length=100,required=True)
        seat_count = forms.IntegerField(required=True)
        bus_fk = forms.ModelChoiceField(Bus.objects,required=True)

        def __init__(self, *args, **kwargs):
                super(add_bus_seatForm, self).__init__(*args, **kwargs)
                for visible in self.visible_fields():
                        visible.field.widget.attrs['class'] = 'form-control input-height'
                        visible.field.widget.attrs['placeholder'] = 'please Enter Details'

class Add_Special_toursForm(forms.ModelForm):
        class Meta:
                model = Special_Tours
                fields = ['name','boarding_point','dropping_point','offer_per','offer','start_date','end_date','time','bus_fk_k','description','schedule','origin_fk_k','destination_fk_k','price','total_days','img1','img2','img3','img4']
                widgets={
                        'name':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Fullname'}),
                        'offer_per':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Offer per'}),
                        
                        'start_date': forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'date'}),
                        'end_date' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'date'}),
                        'time' : forms.NumberInput(attrs={'class': 'form-control datepicker-default form-control picker__input','type':'time'}),
                        'bus_fk_k':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'description' : forms.Textarea(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Descripion'}),
                        'schedule' : forms.Textarea(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Schedule'}),
                        'origin_fk_k':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'destination_fk_k':forms.Select(attrs={'class':'form-select','type':'input'}),
                        'price':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Price for tour'}),
                        'total_days':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter total days'}),
                        'boarding_point':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Boarding Point'}),
                        'dropping_point':forms.TextInput(attrs={'class':'form-control input-height','type':'input','placeholder':'Enter Dropping Point'})
                }



