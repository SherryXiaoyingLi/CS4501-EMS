from django import forms

#Form to login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, help_text="Username: ")
    password = forms.CharField(max_length=200, help_text="Password: ")
    is_consumer = forms.BooleanField(required=False)
    
# Form to delete an authenticator
class EnterAuthenticatorForm(forms.Form):
    authenticator = forms.CharField(max_length=256, help_text="Authenticator: ")
