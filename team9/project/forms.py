from django import forms

from django.contrib.auth.models import User
from project.models import *

class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username



class ProfileOverview(forms.Form):
	username = forms.CharField(max_length = 160)
	email = forms.CharField(max_length = 160)
	old_password = forms.CharField(max_length = 16, label = 'Password', widget = forms.PasswordInput())
	password1 = forms.CharField(max_length = 16, label = 'Password', widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 16, label = 'Confirm password', widget = forms.PasswordInput())
	phoneNum = forms.CharField(max_length = 20)
	ConfirmNum = forms.CharField(max_length = 5)

	def clean(self):
		cleaned_data = super(ProfileOverview, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

class ProfileNameForm(forms.Form):
	username = forms.CharField(max_length = 160)
	email = forms.CharField(max_length = 160)

class ProfilePswForm(forms.Form):
	old_password = forms.CharField(max_length = 16, label = 'Old Password', widget = forms.PasswordInput(attrs={'size': 20,}))
	password1 = forms.CharField(max_length = 16, label = 'New Password', widget = forms.PasswordInput(attrs={'size': 20,}))
	password2 = forms.CharField(max_length = 16, label = 'Confirm password', widget = forms.PasswordInput(attrs={'size': 20,})) 

	def clean(self):
		cleaned_data = super(ProfilePswForm, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

class ProfilePhoneForm(forms.Form):
	phoneNum = forms.CharField(max_length = 20)
	ConfirmNum = forms.CharField(max_length = 5)