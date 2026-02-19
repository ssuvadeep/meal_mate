from django.contrib import admin
from .models import Customer
from .models import Restaurant
from .models import MenuItem
from .models import CartItem
# Register your models here.
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(CartItem)

