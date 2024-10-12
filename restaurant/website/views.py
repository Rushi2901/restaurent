from django.shortcuts import render
from .models import *

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
   


    return render(request,'index.html' , {'offer':offer,'category':category,'item_list':item_list , 'about_desc':about_desc , 'feedback':feedback})

def aboutview(request):
    about_desc = Aboutus.objects.all()

    return render(request,'about.html' , {'about_desc':about_desc})

def menuview(request):
    category = Category.objects.all()
    item_list = Item.objects.all()


    return render(request,'menu.html' , {'category':category,'item_list':item_list})

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

    return render(request,'booktable.html' , {})


def feedback (request):
    if request.method =="POST":
        email = request.POST.get('email')
        rating=  request.POST.get('rating')
        review = request.POST.get('comment')
        image= request.POST.get('image')
        if email!='' and review !='' and rating !='' and image!='' :
            data  = Feedback (email=email,rating= rating,image=image,review=review)
            data.save()




    return render(request,'feedback.html' , {})