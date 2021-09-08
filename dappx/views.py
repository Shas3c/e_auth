from django.shortcuts import render
from dappx.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from random import randint
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request,'dappx/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'dappx/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user1 = User.objects.get(username=username)
            user_email = user.email
            if 'loginbtn' in request.POST and user.is_active:
                otp = randint(100000, 999999)
                print(otp)
                subject = "Login with OTP"
                sender = settings.EMAIL_HOST_USER
                message = "Hi,"+ str(user.first_name)+", this is your OTP for logging into our system : " + str(otp) + ". Please login within 5 minutes."
                val = send_mail(subject, message, sender, [user_email])
                if val:
                    request.session['username']=username
                    request.session['password']=password
                    request.session['otp']=otp
                    return HttpResponseRedirect(reverse(otp_validator))
                    
                else:
                    return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'dappx/login.html', {})

def otp_validator(request):
    return render(request,'dappx/opt_validator.html')

def OTPAuthentication(request):
    if request.method == 'POST' and (request.session['username'] and request.session['password'] and request.session['otp']):
        OTP2 = request.POST['OTP']
        username = request.session['username']
        password = request.session['password']
        otp = request.session['otp']
        if (str(otp) == str(OTP2)):
            user=auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            return HttpResponseRedirect(reverse(index))
        else:
            messages.info(request, 'Invalid OTP.')
            return render(request, 'dappx/login.html')
       