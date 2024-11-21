from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Category (models.Model):
    category_name =models.CharField(max_length=50,blank=False,primary_key=True)

    def __str__(self):
        return self.category_name


class Item (models.Model):
    item_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category,related_name='item_category',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.item_name


class Aboutus (models.Model):
    description = models.TextField(blank=False)



class BookTable (models.Model):
    name = models.CharField(max_length=20)
    phone_no=models.IntegerField(blank=False)
    email=models.EmailField(blank=False)
    total_person=models.IntegerField(blank=False)
    booking_date=models.DateField()

    def __str__(self):
        return self.name


class Offersection (models.Model):
    name =  models.CharField(max_length=30)
    percent_off = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='items/')

    def save(self, *args, **kwargs):
        # Check the number of existing records
        if Item.objects.count() >= 2:
            # Get the oldest record (or modify this logic if needed)
            oldest_item = Item.objects.order_by('id').first()
            # Update the oldest record's data
            oldest_item.name = self.name
            oldest_item.percent_off = self.percent_off
            oldest_item.image = self.image
            oldest_item.save()
        else:
            # If there are fewer than 2 records, create a new one
            super().save(*args, **kwargs)   
    def __str__(self):
            return self.name + "  percent_off:" + str(self.percent_off)
    


class Feedback (models.Model):
    email=models.EmailField(blank=True)
    rating=models.IntegerField(blank=False)
    review = models.TextField(blank=False)
    image= models.ImageField(blank=True)

    def __str__(self):
        return self.email + "   rating:" +str(self.rating)
    
class Footer (models.Model):
    phone =models.IntegerField(max_length=10 ,blank=False)
    email = models.EmailField(blank=True)
    about = models.CharField(max_length=100 , blank=False)
    copyright = models.CharField(max_length=40 , blank=False)
    opening_days = models.CharField(max_length=50 , blank=False)
    opening_time_from =models.IntegerField(max_length=2 )
    opening_time_to =models.IntegerField(max_length=2)

    def clean(self) :
        if not (0< self.opening_time_from >13) and not (0< self.opening_time_to >13):
            raise ValidationError("Hour must be from 1 and 12.")
        
    def save(self, *arg,**kwarg):
        self.clean()
        return super().save(*arg,**kwarg)
    
from django.db import models



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE)  # Assume you have a Product model
    quantity = models.IntegerField(default=1)




class OrderDetails(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    customer_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(OrderDetails, related_name="orderitems", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


from django.contrib import admin
from .models import OrderDetails, OrderItem

# Inline for OrderItem
class OrderItemInline(admin.TabularInline):  # Use TabularInline for a table-like layout
    model = OrderItem
    extra = 0  # No empty extra forms will be shown
    fields = ['product_name', 'quantity', 'unit_price']  # Customize the fields you want to show

# Admin for OrderDetails
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_email', 'total_amount', 'currency', 'status', 'created_at')
    search_fields = ('order_id', 'customer_email')
    inlines = [OrderItemInline]  # Display OrderItems inline as a table

# Admin for OrderItem (optional, depending on if you need to edit items directly in the admin)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'unit_price', 'order')
    search_fields = ('product_name', 'order__order_id')

