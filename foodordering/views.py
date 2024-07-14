from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from instamojo_wrapper import Instamojo
from django.conf import settings
api = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')


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
        
from django.db.models import Q,Count,Max,Sum
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
   
@login_required(login_url='/login')
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




@login_required(login_url='/login')
def cartitems(request):
    # Get the cart object for the current user that is not paid
    cart = Cart.objects.get(is_paid=False, user=request.user)
    
    response=api.payment_request_create(
        amount=cart.get_cart_total(),
        purpose="Order",
        buyer_name="sai",
        email="golisaikrishnareddy95@gamil.com",
        redirect_url="http://127.0.0.1:8898/success/",
       
        
        
    )
    cart.instamojo_id=response['payment_request']['id']
    cart.save()
    
    
    # Get all cart items associated with the cart
    total_price = Cartitems.objects.filter(cart=cart).aggregate(total_price=Sum('product__product__product_price'))['total_price'] or 0


    context={"cart":cart,"total_price":total_price,'payment_url':response['payment_request']['longurl']}
    return render (request, 'foodordering/cart.html',context)



#remove unwanted cart items 
def remove_cart_items(request,cart_item_uid):
    Cartitems.objects.get(uid=cart_item_uid).delete()
    return redirect("/cat")


def orders(request):
    order=Cart.objects.filter(is_paid=False,user=request.user)
    context={"order":order}
    return render (request, 'foodordering/orders.html',context)


def success(request):
    payment_request_id = request.GET.get('payment_request_id')
    
    # Check if payment_request_id is not None
    if payment_request_id:
        try:
            cart = Cart.objects.get(instamojo_id=payment_request_id)
        except Cart.DoesNotExist:
            return HttpResponse('Cart not found', status=404)
        
        # Assuming cart is found, update its status
        cart.is_paid = True
        cart.save()
        
        # Redirect to '/myorders'
        return redirect('/myorders')  # Assuming 'myorders' is the name of the URL pattern for '/myorders'
    
    else:
        # Handle case where payment_request_id is missing
        return HttpResponse('payment_request_id parameter is missing', status=400)
