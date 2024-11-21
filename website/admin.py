from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Aboutus)
admin.site.register(Feedback)
admin.site.register(BookTable)
admin.site.register(Offersection)
admin.site.register(Footer)
admin.site.register(Cart)
admin.site.register(CartItem)


admin.site.register(OrderDetails, OrderDetailsAdmin)  # Custom admin for OrderDetails
admin.site.register(OrderItem, OrderItemAdmin)  # Custom admin for OrderItem
