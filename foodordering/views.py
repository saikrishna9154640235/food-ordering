from django.shortcuts import render,redirect
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages


def register(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        username=data.get("username")
        email=data.get("email")
        password=data.get("password")
        user=User.objects.filter(username=username)
        if user.exists():
            return redirect('/register')        
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            
        )
        user.set_password(password)
        user.save()
        
        
        return redirect("/login")
    return render(request, 'foodordering/register.html')
        
  
    
from django.db.models import Q
def products (request):
       

    product=ProductImage.objects.all()
    if request.GET.get('search'):
        search=request.GET.get('search')
        product=ProductImage.objects.filter(
            Q(product__product_name__icontains=search)|
            Q(product__product_description__icontains=search)
            )
    context={"product":product}
    return render(request,'foodordering/products.html',context)


def logins(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'invalid user')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is None:

            messages.error(request, 'invalid CREDENTIAL')
            return redirect("/login")



        else:
            login(request, user)

            return redirect('/')  # Redirect to home page after successful login

    return render(request, 'foodordering/login.html') 

def logouts(request):
    logout(request)
    return redirect("/login")


