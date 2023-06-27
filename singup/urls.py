"""skts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.usercreation, name="usercreation"),
    path('login/', views.user_login, name='login'),
    path('adminlogin/', views.admin_login, name='admin_login'),
   path('addteacher/', views.addteacher, name='add_teacher'),
   path('logout', views.logout, name='logout'),
   path('resetpassword', views.resetpassword, name='resetpassword'),
   path('addstudent/', views.addstudent, name='add_student'),
   path('selectclass', views.selectclass, name='selectclass'),
   path('sprofile/<str:username>', views.studenthome, name='studenthome'),
   path('tprofile/<str:username>', views.teacherhome, name='teacherhome'),
#    path('addstudent/', views.addstudent)
    path('enter_marks/<str:selected_class>', views.enter_marks, name='enter_marks'),
    path('examresults', views.examresults, name='examresults'),
   
]
