from django.shortcuts import render

# Create your views here.
def homeview(request):
    return render(request,'menu.html' , {})

def aboutview(request):
    pass

def menuview(request):
    pass

def booktableview(request):
    pass