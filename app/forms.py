# app/forms.py

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, UsernameField,
    PasswordChangeForm, SetPasswordForm, PasswordResetForm
)
from django.contrib.auth.models import User
from .models import Customer, CommunityGroup

# ❗ FIX: Import the choices from the new utils.py file
from .utils import STATE_CHOICES, DISTRICTS_BY_STATE

# Fix: Use same platform choices as model
PLATFORM_CHOICES = CommunityGroup.PLATFORM_CHOICES

# ------------------------
# Login Form
# ------------------------
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password',
        'class': 'form-control'
    }))

# ------------------------
# User Registration Form
# ------------------------
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# ------------------------
# Change Password Form
# ------------------------
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
        'autofocus': True,
        'class': 'form-control',
        'placeholder': 'Enter Old Password'
    }))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter New Password'
    }))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }))

# ------------------------
# Password Reset Form
# ------------------------
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your registered email'
    }))

# ------------------------
# Set New Password Form
# ------------------------
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'class': 'form-control',
        'placeholder': 'Enter New Password'
    }))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }))

# ------------------------
# Customer Profile Form
# ------------------------
class CustomerProfileForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ------------------------
# Community Group Form
# ------------------------
class CommunityGroupForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'id': 'state-add'}))
    district = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'district-input'}),
        required=True
    )

    class Meta:
        model = CommunityGroup
        fields = ['state', 'district', 'region', 'group_name', 'group_link', 'platform']
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group_link': forms.URLInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
        }