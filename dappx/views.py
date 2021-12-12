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
from django.views.decorators.cache import cache_control
import qrcode

location = "/Users/sahilsharma/Downloads/djangoy/"
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
                message = "Hi,"+ str(user1)+" this is your OTP for logging into our system : " + str(otp) 
                val = send_mail(subject, message, sender, [user_email])
                if val:
                    request.session['username']=username
                    request.session['password']=password
                    request.session['otp']=otp
                    return HttpResponseRedirect(reverse(otp_validator))
                    
                else:
                    return HttpResponse("Your account was inactive.")
            elif 'loginbtn2' in request.POST:
                otp2 = randint(100000, 999999)
                qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=5,border=5)
                qr.add_data(username + ' ' + password + ' ' + str(otp2))
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')
                img.save(location+'qrcode_'+str(user.username) +'.png')
                print('QR Code generated!!')
                
                email_sender = settings.EMAIL_HOST_USER
                subject = "Login with QR"
                message = "Hi,"+ str(user1)+", the QR for logging into our system is attached. Please login within 5 minutes."
                mail = EmailMessage(subject,message,email_sender,[user_email])
                mail.attach_file(location+'qrcode_'+str(username)+'.png')
                val = mail.send()
                if val:
                    print('Email was sent successfully')
                    request.session['username']=username
                    request.session['password']=password
                    request.session['otp2']=otp2
                    return HttpResponseRedirect(reverse(qr_code))
                    #return render(request, 'dappx/qr_code.html')
                else:
                    print('Email was not sent successfully')
                    #return redirect('../login')
        else:
            #print("Someone tried to login and failed.")
            #print("They used username: {} and password: {}".format(username,password))
            messages.error(request, 'Invalid Login.')
            return render(request, 'dappx/login.html')
            #return HttpResponse("Invalid login details given")
    else:
        return render(request, 'dappx/login.html', {})

def otp_validator(request):
    return render(request,'dappx/opt_validator.html')

def qr_code(request):
    return render(request,'dappx/qrcode.html')

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
            messages.error(request, 'Invalid OTP.')
            return render(request, 'dappx/login.html')

def QRAuthentication(request):
    if request.method == 'POST' and (request.session['username'] and request.session['password'] and request.session['otp2']):
        #Take the session variable
        username = request.session['username']
        password = request.session['password']
        otp2 = request.session['otp2']
        #Take the variables from QR Code reader template
        credentials = request.POST['b']
        temp = credentials.split(" ")
        username2 = temp[0]
        password2 = temp[1]
        otp3 = temp[2]
        if (str(username)== str(username2) and str(password) ==str(password2) and str(otp2)== str(otp3)):
            user=auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            return HttpResponseRedirect(reverse(index))
        else:
           #print('Invalid credentials!!!')
            messages.error(request,'Invalid QR.')   
            return render(request,'dappx/login.html')
    elif request.method == 'GET' and (request.session['username'] and request.session['password']):
        return render(request,'dappx/qrcode.html')
       