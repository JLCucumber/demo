from djangoProject8.urls import path
from drifter.views import *

urlpatterns=[
    path('login/',login,name='log'),
    path('register/',register,name='reg'),
    path('refloat/',refloat,name="refloat"),
    path('gateway/',gateway,name='gateway'),
    path('baobao/',baobao,name='baobao'),
    path('reply/',reply,name='reply'),
    path('cast/',cast,name='cast'),
    path('user_center/',user_center,name='user_center'),
    path('infor_change/',infor_change,name='infor_change')
]