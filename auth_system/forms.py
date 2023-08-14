from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class registerUser(UserCreationForm):

    class Meta:
        model = CustomUser  #database 
        fields = ('username','first_name','last_name','email','password1', 'password2','contact','gender')
        widgets = {
                'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),
                'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
                'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
                'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
                'contact':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Contact'}),
                'password1':forms.TextInput(attrs={'class':'form-control','type':'password','style':'width:350px'}),
                'password2':forms.TextInput(attrs={'class':'form-control'}),
                # 'gender':forms.CheckboxInput(attrs={'class':"form-group",'type':'checkbox','style':'height:10px'}),
                'gender':forms.RadioSelect(attrs={'class':"form-check-flex list-unstyled ",'type':'radio','style':'height:20px'})
        }
    
class loginUser(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
        
