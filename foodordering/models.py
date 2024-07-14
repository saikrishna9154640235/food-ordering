from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

            

# Create your models here.

class Basemodel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract=True



class Product(Basemodel):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    product_name=models.CharField(max_length=100)
    product_slug=models.SlugField(unique=True)
    product_description=models.TextField()
    product_price =models.IntegerField(default=101)
    products_demo_price=models.IntegerField(default=10)
    quantity=models.CharField(max_length=100,null=True,blank=True)
    
class ProductMetaInformation(Basemodel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="meta_information")
    product_measuring = models.CharField(max_length=100, null=True, blank=True, choices=(("KG","KG") ,("L","L"),("ML","ML"),(None,None)))
    product_quantity = models. CharField(max_length=100,null=True,blank=True)
    is_restrict=models.BooleanField(default=False)
    restrict_quantity=models.IntegerField()


class ProductImage(Basemodel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    product_image=models.ImageField(null=True, blank=True)
    
    
class Cart(Basemodel):
    user=models.ForeignKey(User, null=True,blank=True,on_delete=models.CASCADE,related_name='cart')
    is_paid=models.BooleanField(default=False)
    instamojo_id=models.CharField(max_length=1000)
    def get_cart_total(self):
            return Cartitems.objects.filter(cart=self).aggregate(Sum("product__product__product_price"))['product__product__product_price__sum']
    
     
     
class Cartitems(Basemodel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product=models.ForeignKey(ProductImage,on_delete=models.CASCADE,related_name='cart_items')    
    
        
    
