from django.shortcuts import render
from .models import Banner,VisionMission,Statistic,Initiative

# Create your views here.
#Home Page View
def show(request):
    banners = Banner.objects.filter(status=True).order_by('order')
    vision_mission = VisionMission.objects.last()
    statistics = Statistic.objects.filter(status="Active").order_by('order')
    initiatives = Initiative.objects.filter(status="Active").order_by('order')
    context = {
        'banners': banners,
        'vision_mission': vision_mission,
        'statistics': statistics,
        'initiatives': initiatives,
    }
    return render(request, 'home.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterationForm, LoginForm, ngoBannerCrud, VisionMissionForm,StatisticForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Register view
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

# Step 1: Register view (store in session, send OTP) 
def registerView(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST) 
        if form.is_valid():
            # Save data in session temporarily
            request.session['user_data'] = form.cleaned_data 
            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)

            # Send OTP via email
            send_mail(
                subject='Your OTP for Registration',
                message=f'Your OTP is: {otp}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
                fail_silently=False,
            )
            return redirect('verify_otp')  # Redirect to OTP page
    else:
        form = UserRegisterationForm()
    return render(request, 'register.html', {'form': form})  

# Step 2: OTP verification view 
def verifyOTPView(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        print("Entered OTP:", entered_otp)
        print("Session OTP:", request.session.get('otp'))
        if entered_otp == request.session.get('otp'):
            data = request.session.get('user_data')
            if data:
                user = User(
                    email=data['email'],
                    full_name=data['full_name'],
                    role=data['role']
                )
                user.set_password(data['password1'])
                user.save()
                messages.success(request, "Account created successfully!")
                # Clear session data
                request.session.flush()
                return redirect('login')
        messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'verify_otp.html')

import datetime
# Login view
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['last_activity']=str(datetime.datetime.now())
                request.session.set_expiry(1800)
                response=redirect('home')
                request.session['email']=email
                response.set_cookie('Emailis',email)
                response.set_cookie('time',datetime.datetime.now())
                return response
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form}) 

# Logout view
def logoutView(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')

#Manage View - Admin Panel (Banner, Vision, Mission, Statistics)
def manage(request):
    return render(request,'manage.html')

def managehome(request):
    return render(request,'managehome.html')

def manageslider(request):
    if request.method=='POST':
        ngoBanner=ngoBannerCrud(request.POST,request.FILES)
        if ngoBanner.is_valid():
            ngoBanner.save()
            return redirect('managehome')
        else:
            return redirect('manageslider')
    else:
        form=ngoBannerCrud() 
        banners = Banner.objects.all().order_by('order')
        return render(request,'manageslider.html',{'form':form,'banners':banners})
    
def edit_banner(request, id):
    banner = get_object_or_404(Banner, id=id)

    if request.method == 'POST':
        form = ngoBannerCrud(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('manageslider') 
    else:
        form = ngoBannerCrud(instance=banner)

    return render(request, 'edit_banner.html', {'form': form, 'banner': banner})


def delete_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    return redirect('manageslider')

def managevisionmission(request):
    if request.method=='POST':
        ngovisionmission=VisionMissionForm(request.POST)
        if ngovisionmission.is_valid():
            ngovisionmission.save()
            return redirect('managehome')
        else:
            return redirect('managevisionmission')
    else:
        form=VisionMissionForm() 
        vision_mission = VisionMission.objects.all().order_by('-last_updated')
        return render(request,'managevisionmission.html',{'form':form,'vision_mission':vision_mission})
    
def edit_vision_mission(request, id):
    vm = get_object_or_404(VisionMission, id=id)
    if request.method == 'POST':
        form = VisionMissionForm(request.POST, instance=vm)
        if form.is_valid():
            form.save()
            return redirect('managevisionmission')
    else:
        form = VisionMissionForm(instance=vm)
    
    vision_mission = VisionMission.objects.all().order_by('-last_updated')
    return render(request, 'editvisionmission.html', {
        'form': form,
        'vision_mission_list': vision_mission
    })

def delete_vision_mission(request, id):
    vm = get_object_or_404(VisionMission, id=id)
    vm.delete()
    return redirect('managevisionmission')

def manage_statistics(request):
    if request.method == 'POST':
        form = StatisticForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managehome')
        else:
            return redirect('manage_statistics')
    else:
        form = StatisticForm()

    statistics = Statistic.objects.all().order_by('order')
    return render(request, 'managestatistic.html', {
        'form': form,
        'statistics': statistics
    })

def edit_statistic(request, id):
    stat = get_object_or_404(Statistic, id=id)
    if request.method == 'POST':
        form = StatisticForm(request.POST, instance=stat)
        if form.is_valid():
            form.save()
            return redirect('manage_statistics')
    else:
        form = StatisticForm(instance=stat)
    statistics = Statistic.objects.all().order_by('order')
    return render(request, 'editstatistic.html', {
        'form': form,
        'statistics': statistics
    })

def delete_statistic(request, id):
    stat = get_object_or_404(Statistic, id=id)
    stat.delete()
    return redirect('manage_statistics')

# Password reset views
import random
from django.contrib import messages 
from django.core.mail import send_mail 

def forgotpassword(request):
    if request.method == 'POST':
        email= request.POST.get('email')

        users=User.objects.filter(email=email)
        if users.exists():
            user=users.first()
            otp=random.randint(100000,999999)
            request.session['reset_otp']=otp
            request.session['reset_email']=email
            request.session['otp_purpose']="login"

            subject = "Your Password Reset OTP"  
            message = f"Dear {user.full_name},\n\nYour OTP for passsword reset is: {otp}\n\nPlease enter proper OTP to reset password and It will be valid for 5 minute.\n\nBest Regards,\nHelping Heart Support Team."

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('verifyotp')
        
        else:
            messages.error(request,"Email not found! Please enter a registered email.")
            return render(request,'forgotpassword.html')
    
    return render(request,'forgotpassword.html')
        
def verifyotp(request):
    if request.method == 'POST':
        enterotp=request.POST.get('otp')
        storedotp=request.session.get('reset_otp')
        otppurpose=request.session.get('otp_purpose','')

        if storedotp and enterotp == str(storedotp):
            if otppurpose == 'login':
                return redirect('resetpassword')
            elif otppurpose == 'payment':
                return redirect('paypalsuccess')
            else:
                return redirect('home')
            
        else:
            messages.error(request,'Invalid OTP! Please Try Again.')  

    return render(request,'verifyotp.html')  
        
def resetpassword(request):
    if request.method == 'POST':
        newpassword=request.POST['new_password']
        confirmpassword=request.POST['confirm_password']
        email=request.session.get('reset_email')

        if newpassword == confirmpassword:
            try:
                user = User.objects.get(email=email)
                user.set_password(newpassword)
                user.save()

                # Clear session data: 
                del request.session['reset_otp']
                del request.session['reset_email']

                messages.success(request,"Password reset successfull! You can login now!")
                return redirect('login')
            
            except User.DoesNotExist:
                messages.error(request,"Something went wrong!! Try Again!!")
                return redirect('forgotpassword')
        else:
            messages.error(request,'Password do not match !! Try Again!!')
            return render(request,'resetpassword.html')
        
    return render(request,'resetpassword.html')