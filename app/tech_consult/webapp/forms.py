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


class UpdateReviewForm(forms.Form):
    rating = forms.IntegerField(help_text="Rating: ")
    comment = forms.CharField(max_length=150, help_text="Comment: ")
    author = forms.IntegerField(help_text="Author PK: ")
    producer =forms.IntegerField(help_text="Producer PK: ")


class UpdateConsumerRequestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text="Title: ")
    offered_price = forms.FloatField(help_text="Offered Price: ")
    description = forms.CharField(max_length=200, help_text="Description: ")
    timestamp = forms.CharField(max_length=200, help_text="Timestamp: ")
    availability = forms.CharField(max_length=15, help_text="Availability: ")
    consumer = forms.IntegerField(help_text="Consumer PK: ")
    accepted_producer = forms.IntegerField(help_text="Producer PK: ")
