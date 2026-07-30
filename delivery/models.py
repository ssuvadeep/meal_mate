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
    MenuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('Customer', 'MenuItem')

    def line_total(self):
        return self.MenuItem.price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-placed_at']

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.price * self.quantity