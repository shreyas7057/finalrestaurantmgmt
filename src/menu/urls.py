from django.urls import path
from .views import all_foods_menu_page,food_details,food_filter_dessert,food_filter_starters,food_filter_main_course,food_filter_cold_drinks,addTocart,cart,delete_from_cart,placeOrder,success_order,invoice_order,my_orders,menu_order_course
from django.conf.urls import url


urlpatterns = [
    path('menu/', all_foods_menu_page, name='menu'),
    path('desserts/', food_filter_dessert, name='desserts'),
    path('starters/', food_filter_starters, name='starters'),
    path('main-course/', food_filter_main_course, name='main-course'),
    path('cold-drinks/', food_filter_cold_drinks, name='cold-drinks'),
    path('food_details/<int:id>',food_details,name='food_details'),

    path('add-to-cart/<str:foodID>/<str:userID>',addTocart,name='addToCart'),
    path('cart/',cart,name='cart'),
    path('delete-cart/<int:id>',delete_from_cart,name='delete_from_cart'),
    path('',delete_from_cart,name='delete_from_cart'),


    path('placeOrder/',placeOrder,name='placeOrder'),

    path('sucessOrder/',success_order,name='success_order'),

    path('invoice/<int:id>',invoice_order,name='invoice_order'),

    path('menu_order_course/',menu_order_course,name='menu_order_course'),
    
    path('myorders/',my_orders,name='myorders'),
    # path('recent_order/',recent_order,name='recent_order'),
]