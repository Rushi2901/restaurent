from django.shortcuts import render

# Create your views here.
def homeview(request):
    return render(request,'index.html' , {})

def aboutview(request):
    return render(request,'about.html' , {})

def menuview(request):
    return render(request,'menu.html' , {})

def booktableview(request):
    return render(request,'booktable.html' , {})