from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    address = models.TextField(max_length=500)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='restaurant_pictures/')
    cuisine = models.CharField(max_length=100)
    rating = models.FloatField()

class MenuItem(models.Model):
    picture = models.URLField(max_length=500)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    vegetarian = models.BooleanField(default=False)

class CartItem(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    MenuItem = models.ManyToManyField("MenuItem", related_name='cart_items')

    def total_price(self):
        return sum(MenuItem.price for MenuItem in self.MenuItem.all())

    

