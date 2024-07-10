from django.apps import AppConfig


class FoodorderingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodordering'
    
    def ready(self):
        from django.contrib.auth.models import User
        def get_cart_count(self):
            from .models import Cartitems
            return Cartitems.objects.filter(cart__is_paid=False,cart__user=self).count()
        User.add_to_class('get_cart_count',get_cart_count)
    
    
    

