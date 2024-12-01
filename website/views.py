from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = settings.DOMAIN
ngrok_url = settings.NGROK_URL


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
                if user is not None :
                    
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
def updatecart(request):
    # Get or create the cart for the user once
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    def get_cart_items():
        cart_items = CartItem.objects.filter(cart=cart)
        return [
            {
                'id': item.product.id,
                'title':item.product.item_name,
                'image': item.product.image.url,
                'description': item.product.description,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': item.quantity * item.product.price,
            } for item in cart_items
        ], sum(item.quantity * item.product.price for item in cart_items)

    # For GET requests, render the HTML page
    if request.method == 'GET':
        items, total_cost = get_cart_items()
        return render(request, 'cart.html', {'items': items, 'total_cost': total_cost})

    # Handle POST requests for AJAX cart updates
    elif request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            action = data.get('action') 
            print(action)
            item_id = data.get('item_id')
            

            # Validate item_id and retrieve product
            if not item_id:
                return JsonResponse({'success': False, 'message': 'Invalid item_id'}, status=400)
            product = get_object_or_404(Item, id=item_id)
           
            # Update cart items based on action
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if action == 'add':
                cart_item.quantity += 1
                print('product add')
                cart_item.save()
            elif action == 'remove' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                print('product subtract')
                cart_item.save()
            elif action == 'delete':
                print('product delete')
                cart_item.delete()

            # Get updated cart items and total cost for the response
            items, total_cost = get_cart_items()
            response_data = {
                'success': True,
                'items': items,
                'total_cost': total_cost
            }

            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print('response render')
                return JsonResponse(response_data)

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



def checkout_session(request):
    if request.method == 'POST':
        try:
            user_email = request.user.email
            user = Cart.objects.get(user=request.user)

            def get_cart_items():
                cart_items = CartItem.objects.filter(cart=user)
                return [
                    {
                        'id': item.product.id,
                        'title': item.product.item_name,
                        'image': ngrok_url + item.product.image.url,
                        'description': item.product.description,
                        'quantity': item.quantity,
                        'price': item.product.price,
                        'total_price': item.quantity * item.product.price,
                    } for item in cart_items
                ]

            cart_item = get_cart_items()
            line_items = []

            for item in cart_item:
                product_price = item['price'] * 100  # Convert to cents
                line_items.append(
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(product_price),
                            'product_data': {

                                'name': item['title'],
                                'description': item['description'],
                                'images': [item['image']],
                            },
                        },
                        'quantity': int(item['quantity']),
                    }
                )
            metadata = {}
            for idx, item in enumerate(cart_item):
                metadata[f"product_{idx}_id"] = item["id"]
                metadata[f"product_{idx}_name"] = item["title"]
                metadata[f"product_{idx}_quantity"] = item["quantity"]

            success_url =  ngrok_url + 'success/'  # Your ngrok URL
            cancel_url = ngrok_url+'cancel/'    # Your ngrok URL
            # Ensure this is a valid URL

            
            print("Success URL:", success_url)  # Debugging output
            print("Cancel URL:", cancel_url)    # Debugging output

            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                billing_address_collection='required',
                success_url= success_url,
                cancel_url= cancel_url ,
                customer_email=user_email,
                metadata=metadata,
            )

            return redirect(checkout_session.url)
        except Exception as error:
            print(f"Error creating checkout session: {error}")  # Print error details
            return render(request, 'error.html', {'error': str(error)})

    return render(request, 'error.html')



@csrf_exempt 
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.WEBHOOK_SECRET_KEY  # Get this from Stripe Dashboard

    try:
        # Verify the event
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Signature verification failed: {e}")
        return HttpResponse(status=400)



    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_email = session.get("customer_email")
        metadata = session.get("metadata", {})
        total_amount = session.get("amount_total") / 100  # Convert cents to dollars
        currency = session.get("currency")
        print( user_email , metadata,total_amount,currency)
        # Save order
        order = OrderDetails.objects.create(
            customer_email=User.objects.get(email=user_email),
            order_id=session["id"],
            total_amount=total_amount,
            currency=currency,
            status="Paid",
        )

        # Save order items
        idx = 0
        while f"product_{idx}_id" in metadata:
            OrderItem.objects.create(
                order=order,
                product_id=metadata[f"product_{idx}_id"],
                product_name=metadata[f"product_{idx}_name"],
                quantity=int(metadata[f"product_{idx}_quantity"]),
                unit_price=total_amount,  # Adjust this based on your price logic
            )
            idx += 1
        user = User.objects.get(email=user_email)
        if user:
                    try:
                        cart = Cart.objects.get(user=user)
                        cart.items.all().delete()  # Delete all cart items for the user
                        cart.delete()  # Optionally delete the cart itself
                    except Cart.DoesNotExist:
                        print('No cart found for user')
                        # Handle the case if no cart exists for the user

    return HttpResponse(status=200)



def success(request):
    return render(request,'success.html')

def cancel(request):
    return render(request,'error.html')


