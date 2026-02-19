from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from .models import Customer
from .models import Restaurant
from .models import MenuItem  
from .models import CartItem

# Create your views here.
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
        # Here you would typically save the user to the database
        #creating customer object and saving to database
        try:
            Customer.objects.get(username=username)
            return HttpResponse("Username already exists. Please choose a different username.")
            
        except:   
            Customer.objects.create(username=username, 
                                password=password, 
                                email=email, 
                                mobile=mobile, 
                                address=address)
        return render(request, 'signin.html')
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Customer.objects.get(username=username, password=password)
            if username == "Suvadeep":
                return render(request, "admin_home.html")
            else:
                 # ✅ Fetch all restaurants for customer view
                restaurants = Restaurant.objects.all()
                return render(request, "customer_home.html", {
                    'restaurants': restaurants,
                     'username': username
                    })
        except Customer.DoesNotExist:
            return render(request, 'fail.html')

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
        
        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {'restaurants': restaurants})
    return render(request, 'add_restaurant.html')
    
def view_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'display_restaurant.html', {'restaurants': restaurants})
    
def open_update_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return render(request, 'update_restaurant.html', {'restaurant': restaurant})
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant not found.")
    
def update_restaurant(request, restaurant_id):
    if request.method == 'POST':
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            restaurant.name = request.POST.get('name')
            restaurant.picture = request.POST.get('picture')
            restaurant.cuisine = request.POST.get('cuisine')
            restaurant.rating = request.POST.get('rating')
            restaurant.save()
            return redirect('view_restaurant_page')  # use the named URL pattern for the list page
        except Restaurant.DoesNotExist:
            return HttpResponse("Restaurant not found.")

def delete_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.delete()
        return redirect('view_restaurant_page')  # use the named URL pattern for the list page
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant not found.")
    
def view_menu(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        # Assuming you have a MenuItem model related to Restaurant
        menu_items = restaurant.menu_items.all()  # Adjust based on your actual model relationship
        return render(request, 'view_menu.html', {'restaurant': restaurant, 'menu_items': menu_items})
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant not found.")

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
        return redirect('view_menu', restaurant_id=restaurant.id)

    return render(request, 'add_menu_item.html', {'restaurant': restaurant})

def customer_view_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()  # Adjust based on your actual model relationship
    return render(request, 'customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username': username
    })
    
def add_to_cart(request, item_id, username):
    item = MenuItem.objects.get(id=item_id)
    customer = Customer.objects.get(username=username)
    cart, created = CartItem.objects.get_or_create(Customer=customer)
    cart.MenuItem.add(item)
    cart.save()
    return HttpResponse(f"Added {item.name} to {username}'s cart.")

def show_cart(request, username):
    customer = Customer.objects.get(username=username)
    cart = get_object_or_404(CartItem, Customer=customer)
    items = cart.MenuItem.all()
    total = cart.total_price()
    return render(request, 'gotocart.html', {
        'items': items,
        'total': total,
        'username': username
    })

def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = get_object_or_404(CartItem, Customer=customer).first()
    cart_items = cart.MenuItem.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'message': "Your cart is empty.",
        })
    