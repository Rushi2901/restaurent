from django.db import models

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

class Feedback (models.Model):
    user_name=models.CharField(max_length=20)
    description= models.TextField(blank=False)
    rating=models.IntegerField()

    def __str__(self):
        return self.user_name + "  rating" + self.rating


class BookTbale (models.Model):
    name = models.CharField(max_length=20)
    phone_no=models.IntegerField(blank=False)
    email=models.EmailField(blank=False)
    total_person=models.IntegerField(blank=False)
    booking_date=models.DateField()

    def __str__(self):
        return self.name
