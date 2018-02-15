from django.forms import ModelForm
from django import forms
from .models import Consumer, ConsumerRequest, Producer, Review

#Form to create or update a consumer
class UpdateConsumerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    first_name = forms.CharField(max_length=200, help_text="First Name: ")
    last_name = forms.CharField(max_length=200, help_text="Last Name: ")
    phone = forms.CharField(max_length=15, help_text="Phone Number: ")
    email = forms.CharField(max_length=200, help_text="Email Address: ")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Consumer
        fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'email')

class UpdateProducerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    first_name = forms.CharField(max_length=200, help_text="First Name: ")
    last_name = forms.CharField(max_length=200, help_text="Last Name: ")
    phone = forms.CharField(max_length=15, help_text="Phone Number: ")
    email = forms.CharField(max_length=200, help_text="Email Address: ")
    bio = forms.CharField(max_length=250, help_text="Bio: ")
    skills = forms.CharField(max_length=200, help_text="Skills: ")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Producer
        fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'email', 'bio', 'skills')
