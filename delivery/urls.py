from django.urls import path
from . import views

urlpatterns = [
    path('', 
         views.index,
           name='home'),
           
    path('open_signin/',
          views.open_signin, 
          name='open_signin'),

    path('open_signup/', 
         views.open_signup,
           name='open_signup'),

    path('signup',
          views.signup,
            name='signup'),

    path('signin', 
         views.signin, 
         name='signin'),

    path('admin_home/', 
         views.admin_home,
           name='admin_home'),

    path('customer_home/<str:username>/',
          views.customer_home,
            name='customer_home'),

    path('add_restaurant_page/',
          views.add_restaurant_page,
            name='add_restaurant_page'),

    path('add_restaurant/', 
         views.add_restaurant,
           name='add_restaurant'),

    path('view_restaurant_page/', 
         views.view_restaurant_page, 
         name='view_restaurant_page'),

    path('open_update_restaurant/<int:restaurant_id>/', 
         views.open_update_restaurant, 
         name='open_update_restaurant'),

    path('update_restaurant/<int:restaurant_id>/',
          views.update_restaurant,
            name='update_restaurant'),

    path('delete_restaurant/<int:restaurant_id>/', 
         views.delete_restaurant,
           name='delete_restaurant'),

    path('view_menu/<int:restaurant_id>/',
          views.view_menu, 
          name='view_menu'),

    path('add_menu_item/<int:restaurant_id>/',
          views.add_menu_item, 
          name='add_menu_item'),

    path('open_edit_menu_item/<int:item_id>/', 
         views.open_edit_menu_item,
           name='open_edit_menu_item'),

    path('edit_menu_item/<int:item_id>/',
          views.edit_menu_item,
            name='edit_menu_item'),

    path('delete_menu_item/<int:item_id>/', 
         views.delete_menu_item, 
         name='delete_menu_item'),

    path('customer_view_menu/<int:restaurant_id>/<str:username>/',
          views.customer_view_menu, 
          name='customer_view_menu'),

  path('add_to_cart/<int:item_id>/<str:username>/',
         views.add_to_cart,
         name='add_to_cart'),

    path('increase_cart_item/<int:item_id>/<str:username>/',
         views.increase_cart_item,
         name='increase_cart_item'),

    path('decrease_cart_item/<int:item_id>/<str:username>/',
         views.decrease_cart_item,
         name='decrease_cart_item'),

    path('remove_from_cart/<int:item_id>/<str:username>/',
         views.remove_from_cart,
         name='remove_from_cart'),

    path('show_cart/<str:username>/', 
         views.show_cart, 
         name='show_cart'),

    path('checkout/<str:username>/', 
         views.checkout, 
         name='checkout'),

      path('payment_success/<str:username>/',
         views.payment_success,
         name='payment_success'),

      path('order_history/<str:username>/',
         views.order_history,
         name='order_history'),
]