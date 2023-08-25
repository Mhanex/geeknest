from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


from django.core.validators import EmailValidator #import to validate email since django validator has been overide
from django import forms #form is needed inside the validator

class UserRegistration(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','members']


        

class UpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar']
        #fields = ['username', 'email']

        