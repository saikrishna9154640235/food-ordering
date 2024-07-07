from django.urls import path
from  . import views



urlpatterns=[
    path("register",views.register , name='register'),
    path('login',views.logins, name='login'),
    path("",views.products),
    path("logout",views.logouts),
    path('see/<uuid:uid>/', views.see_sep, name='see'),
    path('meta/<uuid:metas>',views.meta)



]