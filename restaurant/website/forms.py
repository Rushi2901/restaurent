from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from .models import UserDetail

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

from django import forms

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,  # Standard max_length for Django usernames
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Enter a valid username.'
        }
    )
    
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        error_messages={
            'required': 'Password is required.',
        }
    )


# Create Add Record Form
# class UserDetail (forms.ModelForm):
# 	first_name=forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder': 'First Name'}))
# 	last_name=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name '}))
# 	email=forms.EmailField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address '}))
# 	phone=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number '}))
# 	address=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address '}))
# 	city=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'City '}))
# 	state=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'State '}))
# 	zipcode=forms.CharField(required=True , label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code '}))
	
# 	class Meta :
# 		model = UserDetail
# 		exclude = ('user',)