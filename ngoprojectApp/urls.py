from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.show,name='home'),
    path('', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('verify-otp/', views.verifyOTPView, name='verify_otp'),
    path('logout/', views.logoutView, name='logout'),
    path('forgotpass/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('verifyotp/',views.verifyotp,name='verifyotp'),
    path('manage/',views.manage,name='manage'),
    path('managehome/',views.managehome,name='managehome'),
    path('mangeslider/',views.manageslider,name='manageslider'),
    path('edit-banner/<int:id>/', views.edit_banner, name='edit_banner'),
    path('delete-banner/<int:id>/', views.delete_banner, name='delete_banner'),
    path('managevisionmission/',views.managevisionmission,name='managevisionmission'),
    path('vision-mission/edit/<int:id>/', views.edit_vision_mission, name='edit_vision_mission'),
    path('vision-mission/delete/<int:id>/', views.delete_vision_mission, name='delete_vision_mission'),
    path('statistics/', views.manage_statistics, name='manage_statistics'),
    path('statistics/edit/<int:id>/', views.edit_statistic, name='edit_statistic'),
    path('statistics/delete/<int:id>/', views.delete_statistic, name='delete_statistic'),
    path('profile/', views.profile, name='profile'),
]