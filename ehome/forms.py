from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm ,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import *

#this is a customer registration form #
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email','username','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

# User login form #
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))  
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
  
 # Change Password Form #
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'cuurent-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password1 = forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

# Password Reset Form # 
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=80,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

# User Set Password #
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new_password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

# Customer Profile Form #
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name','phone', 'email', 'locality', 'city', 'zipcode', 'state']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'phone':forms.NumberInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        'state':forms.TextInput(attrs={'class':'form-control'})}