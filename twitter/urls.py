from django.conf.urls import url
import django.contrib.auth.views
from django.urls import path,include
from . import views
app_name='twitter'

urlpatterns=[
    path('top/',views.top_page, name="top"), # リダイレクト
    path('login/', # ログイン
         django.contrib.auth.views.login,
         {
             'template_name': 'twitter/login.html',
         },
         name='login'),
    path('logout/', # ログアウト
         django.contrib.auth.views.logout,
         {
             'template_name': 'twitter/logout.html',
         },
         name='logout'),
]