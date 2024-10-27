from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def homeview(request):
    category = Category.objects.all()
    item_list = Item.objects.all()
    offer = Offersection.objects.all()
    about_desc = Aboutus.objects.all()
    feedback = Feedback.objects.all()
    if request.method =="POST":
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_no')
        email = request.POST.get('email')
        total_person=  request.POST.get('total_person')
        booking_date= request.POST.get('booking_date')
        if name !='' and email!='' and phone_number !='' and total_person !='' and booking_date!='' :
            data  = BookTable (name=name,phone_no = phone_number, email=email,total_person= total_person,booking_date=booking_date)
            data.save()
    if request.user.is_authenticated :
        profile = request.user.first_name
    else:
        profile ='Register'

    return render(request,'index.html' , { 'profile':profile, 'offer':offer,'category':category,'item_list':item_list , 'about_desc':about_desc , 'feedback':feedback})

def aboutview(request):
    about_desc = Aboutus.objects.all()
    if request.user.is_authenticated :
        profile = request.user.first_name
    else:
        profile ='Register'

    return render(request,'about.html' , { 'profile':profile,'about_desc':about_desc})

def menuview(request):
    category = Category.objects.all()
    item_list = Item.objects.all()
    if request.user.is_authenticated :
        profile = request.user.first_name
    else:
        profile ='Register'


    return render(request,'menu.html' , { 'profile':profile,'category':category,'item_list':item_list})

def booktableview(request):
    if request.method =="POST":
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_no')
        email = request.POST.get('email')
        total_person=  request.POST.get('total_person')
        booking_date= request.POST.get('booking_date')

        if name !='' and email!='' and phone_number !='' and total_person !='' and booking_date!='' :
            data  = BookTable (name=name,phone_no = phone_number, email=email,total_person= total_person,booking_date=booking_date)
            data.save()
    if request.user.is_authenticated :
            profile = request.user.first_name
    else:
            profile ='Register'

    return render(request,'booktable.html' , { 'profile':profile})


def feedback (request):
    if request.method =="POST":
        email = request.POST.get('email')
        rating=  request.POST.get('rating')
        review = request.POST.get('comment')
        image= request.POST.get('image')
        if email!='' and review !='' and rating !='' and image!='' :
            data  = Feedback (email=email,rating= rating,image=image,review=review)
            data.save()

    if request.user.is_authenticated :
        profile = request.user.first_name
    else:
        profile ='Register'


    return render(request,'feedback.html' , {'profile':profile })

def loginform (request):
    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                
                # Authenticate and login
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                messages.success(request, "You Have Successfully Registered! Welcome!")
                if request.user.is_authenticated :
                    profile = request.user.first_name
                else:
                    profile ='Register'
                return render(request, 'index.html', { 'profile':profile})
    else:
        form = LoginForm()
        return render(request, 'user_cred/login.html', {'form':form})

         
    return render (request, 'user_cred/login.html',{})  


@login_required
def cart (request):
    return render (request,'cart.html',{})



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:  # Check if the user is authenticated successfully
                auth_login(request, user)  # Log in the user
                print("success register")
                messages.success(request, "You Have Successfully Registered! Welcome!")
                return redirect('home')
            else:
                messages.error(request, "Authentication failed. Please try again.")
    else:
        form = SignUpForm()

    return render(request, 'user_cred/register.html', {'form': form})

def logoutUser (request):
    logout(request)
    return redirect('home')
