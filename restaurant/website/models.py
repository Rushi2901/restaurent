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