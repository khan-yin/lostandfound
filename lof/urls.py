from django.urls import path
from . import views

app_name = 'lof'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('wechatlogin/', views.wechatlogin, name='wechatlogin'),
    path('updateinfo/', views.updateinfo, name='updateinfo'),
    path('updateinfo/', views.updateinfo, name='updateinfo'),
    path('searchinfo/', views.searchinfo, name='searchinfo'),
    path('send/', views.SEND.as_view()),
    path('test/', views.Test.as_view()),
    path('getlost/', views.GETLOST.as_view()),
    path('mylost/', views.MYLOST.as_view()),
    path('myfind/', views.MYFIND.as_view()),
    path('getfind/', views.GETFIND.as_view()),
    path('send2/', views.SEND2.as_view()),
    path('changeStatus/', views.changeStatus, name='changeStatus'),
    path('deleterequest/', views.deleterequest, name='deleterequest'),
    path('searchevent/', views.searchevent, name='searchevent'),
    path('cardattention/', views.cardattention, name='cardattention')
]
