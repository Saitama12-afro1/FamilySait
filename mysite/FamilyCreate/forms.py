from attr import fields
from django import forms
from django.contrib.auth import User

from .models import My_Users, Task, My_Room

class RegisterUser(forms.ModelForm):
    password = forms.CharField(label = "password", widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Repeat password", widget=forms.PasswordInput)
    
    
    class Meta:
        model = My_Users
        fields = ('email','first_name', 'last_name','username')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", max_length=100,  widget=forms.PasswordInput)
    
class RoomForm(forms.ModelForm):
    class Meta:
        model = My_Room
        fields = ('name_room',)
    # Task_Type = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)])
    password = forms.CharField(label="password", max_length=100,  widget=forms.PasswordInput)
    
class ConPasForm(forms.Form):
    name_room = forms.CharField(label="name_room", max_length=100)
    password = forms.CharField(label="password", max_length=100,  widget=forms.PasswordInput)