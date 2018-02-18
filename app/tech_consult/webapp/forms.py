from django.forms import ModelForm
from django import forms
from .models import Consumer, ConsumerRequest, Producer, Review

#Form to create or update a consumer
class CreateConsumerForm(forms.Form):
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

# Same as CreateConsumerForm except fields are optional
class UpdateConsumerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ", required=False)
    password = forms.CharField(max_length=200, help_text="Password: ", required=False)
    first_name = forms.CharField(max_length=200, help_text="First Name: ", required=False)
    last_name = forms.CharField(max_length=200, help_text="Last Name: ", required=False)
    phone = forms.CharField(max_length=15, help_text="Phone Number: ", required=False)
    email = forms.CharField(max_length=200, help_text="Email Address: ", required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Consumer
        fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'email')

class CreateProducerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    first_name = forms.CharField(max_length=200, help_text="First Name: ")
    last_name = forms.CharField(max_length=200, help_text="Last Name: ")
    phone = forms.CharField(max_length=15, help_text="Phone Number: ")
    email = forms.CharField(max_length=200, help_text="Email Address: ")
    bio = forms.CharField(max_length=250, help_text="Bio: ")
    skills = forms.CharField(max_length=200, help_text="Skills: ")

# Same as CreateProducerForm except fields are optional
class UpdateProducerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ", required=False)
    password = forms.CharField(max_length=200, help_text="Password: ", required=False)
    first_name = forms.CharField(max_length=200, help_text="First Name: ", required=False)
    last_name = forms.CharField(max_length=200, help_text="Last Name: ", required=False)
    phone = forms.CharField(max_length=15, help_text="Phone Number: ", required=False)
    email = forms.CharField(max_length=200, help_text="Email Address: ", required=False)
    bio = forms.CharField(max_length=250, help_text="Bio: ", required=False)
    skills = forms.CharField(max_length=200, help_text="Skills: ", required=False)

class CreateReviewForm(forms.Form):
    rating = forms.IntegerField(help_text="Rating: ")
    comment = forms.CharField(max_length=150, help_text="Comment: ")
    author = forms.IntegerField(help_text="Author PK: ")
    producer =forms.IntegerField(help_text="Producer PK: ")

# Same as CreateReviewForm except fields are optional
class UpdateReviewForm(forms.Form):
    rating = forms.IntegerField(help_text="Rating: ", required=False)
    comment = forms.CharField(max_length=150, help_text="Comment: ", required=False)
    author = forms.IntegerField(help_text="Author PK: ", required=False)
    producer = forms.IntegerField(help_text="Producer PK: ", required=False)

class CreateConsumerRequestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text="Title: ")
    offered_price = forms.FloatField(help_text="Offered Price: ")
    description = forms.CharField(max_length=200, help_text="Description: ")
    timestamp = forms.CharField(max_length=200, help_text="Timestamp: ")
    availability = forms.CharField(max_length=200, help_text="Availability: ")
    consumer = forms.IntegerField(help_text="Consumer PK: ")
    accepted_producer = forms.IntegerField(help_text="Producer PK: ")

# Same as CreateConsumerRequestForm except fields are optional
class UpdateConsumerRequestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text="Title: ", required=False)
    offered_price = forms.FloatField(help_text="Offered Price: ", required=False)
    description = forms.CharField(max_length=200, help_text="Description: ", required=False)
    timestamp = forms.CharField(max_length=200, help_text="Timestamp: ", required=False)
    availability = forms.CharField(max_length=200, help_text="Availability: ", required=False)
    consumer = forms.IntegerField(help_text="Consumer PK: ", required=False)
    accepted_producer = forms.IntegerField(help_text="Producer PK: ", required=False)