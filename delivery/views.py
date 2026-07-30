from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
import razorpay

from .models import Customer
from .models import Restaurant
from .models import MenuItem
from .models import CartItem
from .models import Order
from .models import OrderItem

ADMIN_USERNAME = "Suvadeep"

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def index(request):
    return render(request, 'index.html')


def open_signin(request):
    return render(request, 'signin.html')


def open_signup(request):
    return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if Customer.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken. Please choose a different one.")
            return render(request, 'signup.html', {
                'email': email, 'mobile': mobile, 'address': address,
            })

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, 'signup.html', {
                'username': username, 'mobile': mobile, 'address': address,
            })

        if Customer.objects.filter(mobile=mobile).exists():
            messages.error(request, "An account with that mobile number already exists.")
            return render(request, 'signup.html', {
                'username': username, 'email': email, 'address': address,
            })

        Customer.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address,
        )
        messages.success(request, "Account created! Please sign in.")
        return render(request, 'signin.html')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Customer.objects.get(username=username, password=password)
        except Customer.DoesNotExist:
            return render(request, 'fail.html')

        if username == ADMIN_USERNAME:
            return redirect('admin_home')
        return redirect('customer_home', username=username)
    return render(request, 'signin.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def customer_home(request, username):
    query = request.GET.get('q', '').strip()
    restaurants = Restaurant.objects.all()
    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) | Q(cuisine__icontains=query)
        )
    return render(request, 'customer_home.html', {
        'restaurants': restaurants,
        'username': username,
        'query': query,
    })


def add_restaurant_page(request):
    return render(request, 'add_restaurant.html')


def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name,
                                   picture=picture,
                                   cuisine=cuisine,
                                   rating=rating)

        messages.success(request, f'"{name}" was added successfully.')
        return redirect('view_restaurant_page')
    return render(request, 'add_restaurant.html')


def view_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'display_restaurant.html', {'restaurants': restaurants})


def open_update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'update_restaurant.html', {'restaurant': restaurant})


def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()
        messages.success(request, f'"{restaurant.name}" was updated.')
        return redirect('view_restaurant_page')
    return render(request, 'update_restaurant.html', {'restaurant': restaurant})


def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    name = restaurant.name
    restaurant.delete()
    messages.success(request, f'"{name}" was deleted.')
    return redirect('view_restaurant_page')


def view_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'view_menu.html', {'restaurant': restaurant, 'menu_items': menu_items})


def add_menu_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        is_veg = request.POST.get('is_veg') == 'on'

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            picture=image_url,
            vegetarian=is_veg
        )
        messages.success(request, f'"{name}" was added to the menu.')
        return redirect('view_menu', restaurant_id=restaurant.id)

    return render(request, 'add_menu_item.html', {'restaurant': restaurant})

def open_edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return render(request, 'edit_menu_item.html', {'item': item, 'restaurant': item.restaurant})


def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.picture = request.POST.get('image_url')
        item.vegetarian = request.POST.get('is_veg') == 'on'
        item.save()
        messages.success(request, f'"{item.name}" was updated.')
        return redirect('view_menu', restaurant_id=item.restaurant.id)
    return render(request, 'edit_menu_item.html', {'item': item, 'restaurant': item.restaurant})


def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    restaurant_id = item.restaurant.id
    name = item.name
    item.delete()
    messages.success(request, f'"{name}" was removed from the menu.')
    return redirect('view_menu', restaurant_id=restaurant_id)

def customer_view_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username': username
    })


def add_to_cart(request, item_id, username):
    item = get_object_or_404(MenuItem, id=item_id)
    customer = get_object_or_404(Customer, username=username)
    cart_item, created = CartItem.objects.get_or_create(
        Customer=customer, MenuItem=item, defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added "{item.name}" to your cart.')
    return redirect('customer_view_menu', restaurant_id=item.restaurant.id, username=username)


def increase_cart_item(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    cart_item = get_object_or_404(CartItem, Customer=customer, MenuItem_id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart', username=username)


def decrease_cart_item(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    cart_item = get_object_or_404(CartItem, Customer=customer, MenuItem_id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('show_cart', username=username)


def remove_from_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    CartItem.objects.filter(Customer=customer, MenuItem_id=item_id).delete()
    messages.success(request, 'Item removed from your cart.')
    return redirect('show_cart', username=username)


def show_cart(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart_items = CartItem.objects.filter(Customer=customer).select_related('MenuItem')
    total = sum(ci.line_total() for ci in cart_items)
    return render(request, 'gotocart.html', {
        'cart_items': cart_items,
        'total': total,
        'username': username
    })


def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart_items = CartItem.objects.filter(Customer=customer).select_related('MenuItem')
    total_price = sum(ci.line_total() for ci in cart_items)

    if not cart_items:
        return render(request, 'checkout.html', {
            'message': "Your cart is empty.",
            'username': username,
        })

    amount_in_paise = int(total_price * 100)
    razorpay_order = razorpay_client.order.create({
        'amount': amount_in_paise,
        'currency': 'INR',
        'payment_capture': 1,
    })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'username': username,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount_in_paise': amount_in_paise,
    })


def payment_success(request, username):
    if request.method != 'POST':
        return redirect('checkout', username=username)

    customer = get_object_or_404(Customer, username=username)
    params_dict = {
        'razorpay_order_id': request.POST.get('razorpay_order_id'),
        'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
        'razorpay_signature': request.POST.get('razorpay_signature'),
    }

    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('checkout', username=username)

    cart_items = CartItem.objects.filter(Customer=customer).select_related('MenuItem')
    total_price = sum(ci.line_total() for ci in cart_items)

    order = Order.objects.create(
        customer=customer,
        total_price=total_price,
        razorpay_order_id=params_dict['razorpay_order_id'],
        razorpay_payment_id=params_dict['razorpay_payment_id'],
    )
    for ci in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item_name=ci.MenuItem.name,
            price=ci.MenuItem.price,
            quantity=ci.quantity,
        )

    cart_items.delete()

    return render(request, 'checkout.html', {
        'order_placed': True,
        'total_price': total_price,
        'username': username,
    })

def order_history(request, username):
    customer = get_object_or_404(Customer, username=username)
    orders = Order.objects.filter(customer=customer).prefetch_related('items')
    return render(request, 'order_history.html', {
        'orders': orders,
        'username': username,
    })