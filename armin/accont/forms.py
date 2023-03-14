from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields
from .models import User

class Profileform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super(Profileform,self).__init__(*args,**kwargs)
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['username'].help_text = None
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' ,'email', 'is_author' , 'special_user']
        

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')