
from django.urls import path
from  lnr.views import *

app_name='login1'

urlpatterns = [
    path('login/',login,name='log'),
    path('register/',register,name='reg')
]