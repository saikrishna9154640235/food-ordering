from django.urls import path
from  . import views



urlpatterns=[
    path("register",views.register , name='register'),
    path('login',views.logins, name='login'),
    path("",views.products,name='products'),
    path("logout",views.logouts),
    path('see/<uuid:uid>/', views.see_sep, name='see'),
    path('addcart/<uuid:product_uid>/',views.add_cart,name="add_cart"),
    path("cat",views.cartitems ,name="cartitems"),
    path("remove_cart_items/<cart_item_uid>",views.remove_cart_items),
    path("remove_cart_items/<cart_item_uid>",views.remove_cart_items , name="remove_cart_items"),
    path("myorders",views.orders,name='orders'),
    path('success/',views.success, name="success")




]