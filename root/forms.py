from django import forms
from datetime import datetime
from root.models import Mailbox,SearchBus

class EmailForm(forms.ModelForm):
    class Meta:
        model = Mailbox
        fields = ['name','email_id','subject','message','contact']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
            'email_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
            'subject': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Subject'}),
            'message': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Your Message','type':'textarea','rows':50,'cols':15}),
            'contact': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your contact number'}),
        }

class search_busForm(forms.ModelForm):
    class Meta:
        model = SearchBus
        fields = ['from_d','to_d','date']
        widgets = {
            'from_d': forms.TextInput(attrs={'class':'form-control','placeholder':'From.....'}),
            'to_d': forms.TextInput(attrs={'class':'form-control','placeholder':'To....'}),
            'date': forms.NumberInput(attrs={'class': 'form-control date-pick','type':'date','min':datetime.now().date})
            
        }
   
                