from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
        
from django.db.models import Q,Count,Max
@login_required(login_url='/login') #redirect when user is not logged in

def products (request):
       

    product=ProductImage.objects.all()
    if request.GET.get('search'):
        search=request.GET.get('search')
        product=ProductImage.objects.filter(
            Q(product__product_name__icontains=search)|
            Q(product__product_description__icontains=search)
            )
    cart=Cartitems.objects.all();
    mat=cart.aggregate(mat=Count('product'))
    context={"mat":mat}    
    context={"product":product,"mat":mat}
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



def see_sep(request,uid  ):
    product=ProductImage.objects.filter(uid =uid)
    image_count= product.aggregate(image_count=Count('product_image'))  # Counting the number of related images

    return render(request,'foodordering/seesep.html',{"product":product,'image_count':image_count})
   

def add_cart(request, product_uid):
    user = request.user
    product = get_object_or_404(ProductImage, uid=product_uid)
    
    # Retrieve or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
    # Ensure you're getting the actual Cart instance from get_or_create result
    if isinstance(cart, tuple):
        cart = cart[0]  # Retrieve the Cart instance from the tuple
    
    # Create a Cartitems instance
    cart_item = Cartitems.objects.create(
        cart=cart,
        product=product
    )
    return redirect('/')



def cartitems(request):
    cart=Cartitems.objects.all()
    context={'cart':cart}
    return render (request, 'foodordering/cart.html',context)