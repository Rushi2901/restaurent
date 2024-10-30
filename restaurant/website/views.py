from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json


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


# def updatecart (request):
#     if request.method == 'POST' and request.get('from') == 'card':
#         item_id = request.POST.get('item_id')
#         change = int(request.POST.get('change'))

#         cart, created = Cart.objects.get_or_create(user=request.user)

#         # Check if the item is already in the cart
#         try:
#             cart_item = CartItem.objects.get(cart=cart, product__id=item_id)
#             # update the quantity
#             cart_item.quantity = max(1, cart_item.quantity + change)
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             # create a new CartItem
#             if change > 0: 
#                 product = get_object_or_404(Item, id=item_id)  # Ensure the product exists
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=change)

#         return JsonResponse({'success': True, 'quantity': cart_item.quantity})

#     return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    

# @login_required
# def updatecart(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data from request body
#             data = json.loads(request.body.decode('utf-8'))  # Decode to ensure proper string format
#             item_id = data.get('item_id')
#             change = data.get('change')

#             print(f"Received item_id: {item_id}, change: {change}")  # Debugging line

#             # Validate item_id and change
#             if not item_id or change is None:
#                 return JsonResponse({'success': False, 'message': 'Invalid item_id or change value'}, status=400)

#             change = int(change)  # Convert change to an integer

#             # Get or create a cart for the current user
#             cart, _ = Cart.objects.get_or_create(user=request.user)

#             try:
#                 # Check if the item is already in the cart
#                 cart_item = CartItem.objects.get(cart=cart, product__id=item_id)
#                 # Update the quantity
#                 cart_item.quantity = max(1, cart_item.quantity + change)
#                 cart_item.save()
#                 return JsonResponse({'success': True, 'quantity': cart_item.quantity})
#             except CartItem.DoesNotExist:
#                 if change > 0:
#                     product = get_object_or_404(Item, id=item_id)  # Ensure the product exists
#                     cart_item = CartItem.objects.create(cart=cart, product=product, quantity=change)
#                     return JsonResponse({'success': True, 'quantity': cart_item.quantity})
#                 else:
#                     return JsonResponse({'success': False, 'message': 'Cannot add item with non-positive quantity'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

#     return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def updatecart(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            action = data.get('action') 
            print(action +'data is processed')
            item_id = data.get('item_id')
            print(item_id)
            change = data.get('change', 0)

            # Validate item_id
            if not item_id:
                return JsonResponse({'success': False, 'message': 'Invalid item_id'}, status=400)

            product = get_object_or_404(Item, id=item_id)


            # Get or create a cart for the current user
            cart, _ = Cart.objects.get_or_create(user=request.user)

            if action == 'add':
                change = int(change)  # Convert change to an integer
                if change <= 0:
                    return JsonResponse({'success': False, 'message': 'Change must be a positive integer'}, status=400)

                # Check if the item is already in the cart
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                # Update the quantity
                cart_item.quantity += change
                print(cart_item)
                cart_item.save()

            elif action == 'remove':
                cart_item = CartItem.objects.filter(cart=cart, product__id=item_id).first()
                if cart_item:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                    else:
                        cart_item.delete()

            elif action == 'delete':
                cart_item = CartItem.objects.filter(cart=cart, product__id=item_id).first()
                if cart_item:
                    cart_item.delete()

            # Prepare response with updated cart details
            cart_items = CartItem.objects.filter(cart=cart)
            response_data = {
                'success': True,
                'items': [
                    {
                        'id': item.product.id,
                        'image': item.product.image.url,
                        'description': item.product.description,
                        'quantity': item.quantity,
                        'price': item.product.price,
                        'total_price': item.quantity * item.product.price,
                    } for item in cart_items
                ],
                'total_cost': sum(item.quantity * item.product.price for item in cart.items.all())
            }

            # Check if the request is an AJAX call
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
            
            # For non-AJAX requests, render the full template
            return render(request, 'cart/cart_page.html', {'cart': cart})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



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
def cartpage(request):
    return render(request,'cart.html',{})