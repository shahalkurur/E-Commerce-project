from django.urls import path
from category import views

urlpatterns = [

    path('store/',views.store,name='store'),
    path('price_filter/',views.price_filter,name='price_filter'),
    path('search/',views.search,name='search'),

    path('category/add_cart/',views.add_cart,name='add_cart'),
    path('category/cart/',views.view_cart,name='cart'),
    path('category/cart_qty_update/', views.cart_qty_update, name='cart_qty_update'),

   # path('category/remove_cart/<int:id>/',views.remove_cart,name='remove_cart'),
    path('category/delete_cart/<int:id>/',views.delete_cart,name='delete_cart'),

   
    path('add_address/', views.add_address, name='add_address'),
    path('check_out',views.check_out,name='check_out'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('order_success/<int:order_id>/',views.order_success,name='order_success'),
    # path('add_addrs/',views.add_adrs,name='add_addrs'),


    path('my-orders',views.orders,name='my-orders'),



    path('dashboard',views.user_dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_details/<str:pk>/',views.order_details,name='order_details'),
    
    path('cancel_order/<int:pk>/',views.cancel_order,name='cancel_order'),
    path('proceed_to_pay/',views.razor_pay),
    
    path('wishlist',views.wish_list,name='wishlist'),
    path('addto_wishlist',views.addtowishlist,name='addto_wishlist'),
    path('delete_wishlist/<int:pk>/',views.delete_wishlist,name='delete_wishlist'),





]