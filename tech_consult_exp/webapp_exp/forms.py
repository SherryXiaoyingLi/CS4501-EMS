from django import forms

#Form to login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    is_consumer = forms.BooleanField(required=False)

class CreateConsumerRequestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text="Title: ")
    offered_price = forms.FloatField(help_text="Offered Price: ")
    description = forms.CharField(max_length=200, help_text="Description: ")
    availability = forms.CharField(max_length=200, help_text="Availability: ")
    consumer = forms.IntegerField(help_text="Consumer PK: ")
    authenticator = forms.CharField(max_length=256, help_text="Authenticator: ")

# Form to delete an authenticator
class EnterAuthenticatorForm(forms.Form):
    authenticator = forms.CharField(max_length=256, help_text="Authenticator: ")

class CreateConsumerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    first_name = forms.CharField(max_length=200, help_text="First Name: ")
    last_name = forms.CharField(max_length=200, help_text="Last Name: ")
    phone = forms.CharField(max_length=15, help_text="Phone Number: ")
    email = forms.CharField(max_length=200, help_text="Email Address: ")

class CreateProducerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    first_name = forms.CharField(max_length=200, help_text="First Name: ")
    last_name = forms.CharField(max_length=200, help_text="Last Name: ")
    phone = forms.CharField(max_length=15, help_text="Phone Number: ")
    email = forms.CharField(max_length=200, help_text="Email Address: ")
    bio = forms.CharField(max_length=250, help_text="Bio: ")
    skills = forms.CharField(max_length=200, help_text="Skills: ")

class UpdateConsumerRequestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text="Title: ", required=False)
    offered_price = forms.FloatField(help_text="Offered Price: ", required=False)
    description = forms.CharField(max_length=200, help_text="Description: ", required=False)
    availability = forms.CharField(max_length=200, help_text="Availability: ", required=False)
    consumer = forms.IntegerField(help_text="Consumer PK: ", required=False)
    # authenticator = forms.CharField(max_length=256, help_text="Authenticator: ", required=False)

class UpdateConsumerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ", required=False)
    password = forms.CharField(max_length=200, help_text="Password: ", required=False)
    first_name = forms.CharField(max_length=200, help_text="First Name: ", required=False)
    last_name = forms.CharField(max_length=200, help_text="Last Name: ", required=False)
    phone = forms.CharField(max_length=15, help_text="Phone Number: ", required=False)
    email = forms.CharField(max_length=200, help_text="Email Address: ", required=False)

#class Meta:
# Provide an association between the ModelForm and a model
#       model = Consumer
#       fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'email')

class UpdateProducerForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ", required=False)
    password = forms.CharField(max_length=200, help_text="Password: ", required=False)
    first_name = forms.CharField(max_length=200, help_text="First Name: ", required=False)
    last_name = forms.CharField(max_length=200, help_text="Last Name: ", required=False)
    phone = forms.CharField(max_length=15, help_text="Phone Number: ", required=False)
    email = forms.CharField(max_length=200, help_text="Email Address: ", required=False)
    bio = forms.CharField(max_length=250, help_text="Bio: ", required=False)
    skills = forms.CharField(max_length=200, help_text="Skills: ", required=False)

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, help_text="Query: ")

class SearchConsumerForm(forms.Form):
    query = forms.CharField(max_length=200, help_text="Query: ")

class SearchProducerForm(forms.Form):
    query = forms.CharField(max_length=200, help_text="Query: ")

class itemClickForm(forms.Form):
    user_id = forms.IntegerField(help_text="User ID: ")
    item_id = forms.IntegerField(help_text="Item ID: ")
