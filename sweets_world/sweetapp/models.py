# appname/models.py

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUsermanager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,password=None,**extra_fields):
      if not email:
        raise ValueError('email required')
    
      email=self.normalize_email(email)
      user=self.model(email=email,**extra_fields)
      user.set_password(password)
      user.save(using=self.db)
      return user
    
    def create_superuser(self,email,password,**extra_fields):
       extra_fields.setdefault('is_staff',True)
       extra_fields.setdefault('is_superuser',True)
       extra_fields.setdefault('is_active',True)

       if extra_fields.get('is_staff') is not True:
          raise ValueError(('super_user must have is_staff true'))
       return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
   username=models.CharField(max_length=30,null=True,blank=True)
   first_name = models.CharField(max_length=30,blank=True,null=True)
   last_name = models.CharField(max_length=30, blank=True,null=True)
   email=models.EmailField(unique=True,blank=True)
   mobile=models.CharField(max_length=30,blank=True,null=True)
   last_login=models.DateTimeField(null=True,blank=True)
   date_joined=models.DateTimeField(default=timezone.now)
   is_staff=models.BooleanField(default=False)
   is_active=models.BooleanField(default=True)
   my_wallet=models.FloatField( default=0.00)


   objects=CustomUsermanager()


   USERNAME_FIELD='email'
   EMAIL_FIELD='email'
   REQUIRED_FIELDS=[]#except email what else need while creating superuser eq: username


   def __str__(self):
        return self.email
    
   def __iter__(self):
        yield self.first_name



class Profile(models.Model):
      user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)#one profile for one account 'one t one fild'
      address=models.CharField(max_length=150,blank=True)
      profile_pic=models.ImageField(blank=True,upload_to='images/')
      city=models.CharField(max_length=150,blank=True)
      state=models.CharField(max_length=150,blank=True)
      country=models.CharField(max_length=150,blank=True)

      def __str__(self):
          return self.user.first_name

   


