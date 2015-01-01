from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm, LoginForm, PasswordChangeForm,PasswordResetForm,PasswordResetForm2
from django.core.urlresolvers import reverse
from .models import RegKey,ResetKey
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
	if request.POST:
		reg_form = RegisterForm(request.POST)
		if reg_form.is_valid():
			reg_form.save()
			messages.success(request,'Regestration competed Successfully.')
			return redirect(reverse('login'))
	else:
		reg_form = RegisterForm()
		
	return render(request,'register.html',{'reg_form':reg_form})
	
def login_view(request):
	next_page = request.GET.get('next','')
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			uoe = form.cleaned_data['username_or_email']
			password = form.cleaned_data['password']
			if '@' in uoe:
				try:
					user = User.objects.get(email=uoe)
					if user.check_password(password):
						if user.is_active:
							user.backend = 'django.contrib.auth.backends.ModelBackend'
							login(request,user)
							if next_page:
								return redirect(next_page)
							else:
								return redirect(reverse('account'))
						else:
							messages.error(request,'Error : Verify Email')
					else:
						messages.error(request,'Error : Invalid Credentials')
				except User.DoesNotExist:
					pass
			else:
				user = authenticate(username=uoe,password=password)
				if user is not None:
					if user.is_active:
						login(request,user)
						if next_page:
							return redirect(next_page)
						else:
							return redirect(reverse('account'))
					else:
						messages.error(request,'Error : Verify Email')
				else:
					messages.error(request,'Error : Invalid Credentials')
	else:
		form = LoginForm()
		
	return render(request,'login.html',{'form':form,'next_page':next_page})
	
@login_required
def logout_view(request):
	logout(request)
	messages.success(request,'LoggedOut Successfully.')
	return redirect(reverse('account'))

def activate_view(request,activation_key):
	temp = get_object_or_404(RegKey,activation_key=activation_key)
	user = temp.user
	user.is_active=True
	user.save()
	temp.delete()
	messages.success(request,'Account activation competed Successfully.')
	return redirect(reverse('login'))
	
def account_view(request):
	return render(request,'account.html',{'user':request.user})
	
@login_required
def password_change_view(request):
	if request.POST:
		form = PasswordChangeForm(request,request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Password Changed successFully.')
			return redirect(reverse('account'))
	else:
		form = PasswordChangeForm(request.user)
		
	return render(request,'password_change.html',{'form':form})

def reset_view(request):
	if request.POST:
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Password Reset email Sent.')
			return redirect(reverse('login'))
	else:
		form = PasswordResetForm()
		
	return render(request,'password_reset.html',{'form':form})

def reset_activate_view(request,activation_key):
	temp = get_object_or_404(ResetKey,activation_key=activation_key)
	user = temp.user
	if request.POST:
		form = PasswordResetForm2(user,request.POST)
		if form.is_valid():
			form.save()
			temp.delete()
			messages.success(request,'Password Changed successFully.')
			return redirect(reverse('login'))
	else:
		form = PasswordResetForm2(user)
	
	return render(request,'password_reset_activate.html',{'form':form,'key':activation_key})
