from app.models import Customer
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext,gettext_lazy as _


class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}

# class UserLoginForm(AuthenticationForm):
#     # username=UsernameField(widget={forms.TextInput(attrs={'autofocus':True,'class':'form-control'})})
#     # password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
   
#     username=forms.CharField(widget={TextInput(attrs={'class':'form-control'})})
#     password=forms.CharField(widget={PasswordInput(attrs={'class':'form-control'})})

# class AuthenticationForm(AuthenticationForm):
#     class Meta:
#         model=User
#         fields=['username','password']
#         widgets={'username':forms.TextInput(attrs={'class':'form-control'}),'password':forms.PasswordInput(attrs={'class':'form-control'})}

class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label=_("Confirm Password"),strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email=forms.CharField(label=_('Email'),widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','zipcode','state']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),'city':forms.TextInput(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'})}

