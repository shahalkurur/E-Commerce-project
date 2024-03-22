from django.db import models
import datetime
import os
from sweetapp.models import CustomUser
from django.utils import timezone
from datetime import timedelta

# Create your models here.
# def get_file(request,filename):
#     original_filename=filename
#     nowtime=datetime.datetime.now().strftime('%Y%M%d%H:%M:%S')
#     filename="%s%s" % (nowtime,original_filename)
#     return os.path.join('uploads/',filename)

class category(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,null=True)
    discription=models.CharField(max_length=200,blank=True)
    cat_image=models.ImageField(upload_to='category/',blank=True)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")


    class Meta :
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return self.category_name
    
class products(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    prod_name=models.CharField(max_length=150,null=False,blank=False)
    prod_image=models.ImageField(upload_to='products',blank=True)
    price=models.FloatField()
    old_price=models.FloatField(null=True)
    dis_price=models.FloatField(null=True)
    stock=models.FloatField()
    is_available=models.BooleanField(default=True)
    description=models.TextField(max_length=200,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    has_offer = models.BooleanField(default=False)


    def __str__(self):
        return self.prod_name


class Cart(models.Model):
      user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
      product=models.ForeignKey(products,on_delete=models.CASCADE)
      quandity=models.PositiveIntegerField(default=1)

      def sub_total(self):
          return self.product.price*self.quandity
class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=20,blank=True,null=True)
    last_name=models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField( unique=False,blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    addressline1 = models.CharField(max_length=255,blank=True,null=True)
    addressline2 = models.CharField(max_length=255,blank=True)
    country = models.CharField(max_length=20,blank=True,null=True)
    state = models.CharField(max_length=20,blank=True,null=True)
    pin = models.CharField(max_length=20,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    
class Order(models.Model):
      user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
      address=models.ForeignKey(Address,on_delete=models.CASCADE)
      total_price=models.FloatField(null=False)
      payment_mode=models.CharField(max_length=150,null=False)
      payment_id=models.CharField(max_length=150,null=True)
      orderstatuses=(
           ('Pending','pending'),
           ('Processing','processing'),
             ('Complete','complete'),
            ('Out for shipping','out for shipping'),
             ('Delivered','delivered'),
             ('Cancel','cancel')
      )
      status=models.CharField(max_length=150,choices=orderstatuses,default='pending')
      message=models.TextField(max_length=150,null=True)
      tracking_no=models.CharField(max_length=150,null=True)
      created_at=models.DateTimeField(auto_now_add=True)
      updated_at=models.DateTimeField(auto_now=True)
      def __str__(self):
           return '{}-{}'.format(self.id,self.tracking_no)


      
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quandity=models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.order.id,self.order.tracking_no)
    
    def sub_total(self):
          return self.product.price*self.quandity


class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Coupen(models.Model):
     code=models.CharField(max_length=15)
     discount=models.IntegerField(null=True)
     start_date=models.DateField()
     end_date=models.DateField()
     is_active=models.BooleanField(default=False)
     mini_amount=models.IntegerField(null=True)
    
class Wallet(models.Model):
     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
     order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
     amount=models.FloatField(default=0.00)
     is_credited=models.BooleanField(default=True)
     created_at=models.DateTimeField(auto_now_add=True)

class ProductOffer(models.Model):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    category = models.ForeignKey(category, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default=FIXED)
    discount_value = models.IntegerField(blank=True)
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    expire_date = models.DateTimeField(blank=True)

    def is_valid_for_category(self):
        time_now = timezone.now()
        
        return self.start_date <= time_now <= self.expire_date











    




    


