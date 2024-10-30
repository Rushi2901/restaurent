from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

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


# class UserDetail(models.Model):
# 	first_name = models.CharField(max_length=50)
# 	last_name =  models.CharField(max_length=50)
# 	email =  models.EmailField()
# 	phone = models.CharField(max_length=15)
# 	address =  models.CharField(max_length=100)
# 	city =  models.CharField(max_length=50)
# 	state =  models.CharField(max_length=50)
# 	zipcode =  models.CharField(max_length=20)

# 	def __str__(self):
# 		return(f"{self.first_name} {self.last_name}")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE)  # Assume you have a Product model
    quantity = models.IntegerField(default=1)
