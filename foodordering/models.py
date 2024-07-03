from django.db import models
import uuid

# Create your models here.

class Basemodel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)

    create_at=models.DateField(auto_created=True)
    update_at=models.DateField(auto_created=True)
    
    class Meta:
        abstract=True



class Product(Basemodel):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    product_name=models.CharField(max_length=100)
    product_slug=models.SlugField(unique=True)
    product_description=models.TextField()
    product_price=models.IntegerField(default=0)
    products_demo_price=models.IntegerField(default=10)
    quantity=models.CharField(max_length=100,null=True,blank=True)
    
    
class ProductMetaInformation(Basemodel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="meta_information")
    product_measuring = models.CharField(max_length=100, null=True, blank=True, choices=(("KG","KG") ,("L","L"),("ML","ML"),(None,None)))
    product_quantity = models. CharField(max_length=100      ,null=True,blank=True)
    is_restrict=models.BooleanField(default=False)
    restrict_quantity=models.IntegerField()


class ProductImage(Basemodel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    product_image=models.ImageField(upload_to='products11')
    
    
