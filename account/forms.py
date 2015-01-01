from django import forms
from django.contrib.auth.models import User
from .models import RegKey,ResetKey
import hashlib,random
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash,login
from django.contrib import messages

class LoginForm(forms.Form):
	username_or_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username or Email'}))
	password = forms.CharField(widget=forms.PasswordInput())	
	
class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput(),label='Old Password')
	password = forms.CharField(widget=forms.PasswordInput(),label='New Password')
	password_again = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
	
	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(PasswordChangeForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		cleaned_data=super(PasswordChangeForm,self).clean()	
		p1 = cleaned_data.get('password')
		p2 = cleaned_data.get('password_again')
		p3 = cleaned_data.get('old_password')
		if p1 and p2 and p3:
			if p1!=p2:
				raise forms.ValidationError('Passwords did not match.')
			if not self.request.user.check_password(p3):
				raise forms.ValidationError('Incorrect old Password.')
		return cleaned_data
	def save(self):
		user = self.request.user
		user.set_password(self.cleaned_data["password"])
		user.save()
		update_session_auth_hash(self.request,user)
		return user
		
class PasswordResetForm(forms.Form):
	username_or_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username or Email'}))
	
	def clean(self):
		cleaned_data=super(PasswordResetForm,self).clean()		
		uoe = cleaned_data.get('username_or_email')
		self.user = None
		if uoe:
			try:
				if '@' in uoe:
					self.user = User.objects.get(email=uoe)
				else:
					self.user = User.objects.get(username=uoe)
			except User.DoesNotExist:
				raise forms.ValidationError('Invalid username or email.')
		return cleaned_data
		
	def save(self):		
		salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()
		email = self.user.email
		key = hashlib.sha1(salt+email).hexdigest()
		try:
			temp = ResetKey.objects.get(user=self.user)
			temp.activation_key=key
			temp.save()
		except ResetKey.DoesNotExist:
			ResetKey.objects.create(user=self.user,activation_key=key)
		
		send_mail('Passwor Reset','http://127.0.0.1:8000/account/reset/'+key+'/','bhargav@ogs.com',[email])
		
		return self.user
		
class PasswordResetForm2(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(),label='New Password')
	password_again = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
	
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(PasswordResetForm2, self).__init__(*args, **kwargs)
	
	def clean(self):
		cleaned_data=super(PasswordResetForm2,self).clean()	
		p1 = cleaned_data.get('password')
		p2 = cleaned_data.get('password_again')
		if p1 and p2 and p1 != p2:
			raise forms.ValidationError('Passwords did not match.')
		return cleaned_data
		
	def save(self):
		user = self.user
		user.set_password(self.cleaned_data["password"])
		user.save()
		return user

class RegisterForm(forms.ModelForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput())
	password_again = forms.CharField(widget=forms.PasswordInput(),label='Password (Again)')
	
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password','password_again']
		
	def clean(self):
		cleaned_data=super(RegisterForm,self).clean()
		p1 = cleaned_data.get('password')
		p2 = cleaned_data.get('password_again')
		if p1 and p2 and p1 != p2:
			raise forms.ValidationError('Passwords did not match.')
		return cleaned_data
		
	def save(self,commit=True):
		user = super(RegisterForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		user.is_active=False
		user.save(commit)
		
		salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()
		email = self.cleaned_data["email"]
		key = hashlib.sha1(salt+email).hexdigest()
		RegKey.objects.create(user=user,activation_key=key)
		
		send_mail('Activate account','http://127.0.0.1:8000/account/activate/'+key+'/','bhargav@ogs.com',[email])
		
		return user
