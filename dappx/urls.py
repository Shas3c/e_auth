# dappx/urls.py
from django.conf.urls import url
from dappx import views
from django.urls import include, path

# SET THE NAMESPACE!
app_name = 'dappx'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('OTPAuthentication/',views.OTPAuthentication,name='OTPAuthentication'),
]