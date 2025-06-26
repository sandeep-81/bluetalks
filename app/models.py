from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser
from random import randint
# Create your models here.

class UserManage(BaseUserManager):
      def create_user(self, email , fullname , password = None):
            if not email :
                  raise "Enter the Valid Email"
            
            user = self.model(email = self.normalize_email(email),fullname = fullname)
            user.set_password(password)
            user.save(using = self._db)
            return user
      
      def create_superuser(self,email, fullname ,password=None , **extra_fields):
            extra_fields.setdefault('is_staff',True)
            extra_fields.setdefault('is_superuser',True)

            if extra_fields.get('is_staff') is not True:
                  raise "Super user must be is_staff True"
            if extra_fields.get('is_superuser') is not True:
                  raise "Super user must be is_superuser True"
            
            user = self.create_user(email ,fullname, password)
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True 
            user.save(using = self._db)
            return user

class User(AbstractBaseUser):
       email = models.EmailField(unique=True , max_length=200)
       fullname = models.CharField(max_length=255)
       about = models.CharField(max_length=400,default="BlueTalks User ")
       is_active = models.BooleanField(default=True) 
       is_superuser = models.BooleanField(default=False)
       is_staff = models.BooleanField(default=False)
       country = models.CharField(max_length=50,default="-")
       state = models.CharField(max_length=50,default="-")
       distt = models.CharField(max_length=50,default="-")
       pincode = models.CharField(max_length=50,default="-")
       search = models.BooleanField(default=True)
       suggest = models.BooleanField(default=True)
       


       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ['fullname']

       objects = UserManage() 
       
       def __str__(self):
            return self.email
       
       def has_perm(self, perm , obj = None):
             return self.is_superuser
       
       def has_module_perms(self,app_label):
             return self.is_superuser
             
       

class FreindRequest(models.Model):
      sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name= "sender")
      rece = models.ForeignKey(User , on_delete=models.CASCADE , related_name="rece")
      status = models.CharField(max_length=50)
      timestamp = models.DateTimeField(auto_now=True)
      room_no = models.CharField(max_length=50, unique=True, blank=True)

      def save(self, *args, **kwargs):
            """ Generate room_no only if it's not set """
            if not self.room_no:
                  self.room_no = f"{self.sender.id}-{self.rece.id}-{randint(1000, 99999)}"
            super().save(*args, **kwargs)

      def __str__(self):
        return f"{self.sender} -> {self.rece} ({self.status}) ({self.room_no})"

class Message(models.Model):
      send_msg = models.ForeignKey(User , on_delete=models.CASCADE , related_name = "send_msg")
      rece_msg =  models.ForeignKey(User , on_delete=models.CASCADE , related_name = "rece_msg")
      message = models.TextField()
      timestamp = models.DateTimeField(auto_now=True)
      is_read = models.BooleanField(default=False)


      def __str__(self):
            return f"{self.send_msg} -> {self.rece_msg} : ({self.message[:20]}) ({self.timestamp}) ({self.id})" 
      
class Themes(models.Model):
      user = models.ForeignKey(User,on_delete=models.CASCADE , related_name="user")
      font = models.CharField(max_length=100 , default="cursive")
      size = models.IntegerField(default=15)
      color_rece = models.CharField(max_length=20,default="Green")
      color_send = models.CharField(max_length=20,default="Red")
      bg1 = models.CharField(max_length=20,default="#262626")
      bg2 = models.CharField(max_length=20,default="#000")
      border = models.CharField(max_length=20,default="#ffffff")

      def __str__(self):
            return f"{self.user} -> {self.font} : ({self.size}) ({self.color_rece}) ({self.color_send}) ({self.bg1} ({self.bg2}) ({self.border})))"
            

