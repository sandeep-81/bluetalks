from django.contrib import admin
from .models import User , FreindRequest , Message , Themes
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserModelAdmin(UserAdmin):
    model = User
    list_display = ['id','email','fullname','about','is_active','is_superuser','is_staff','country','state','distt','pincode','search','suggest']

    list_filter = ['is_superuser']

    fieldsets=[
        ('User Credentials',{'fields':['email','password']}),
        ('Personal Information',{'fields':['fullname','about']}),
        ('Address',{'fields':['country','state','distt','pincode']}),
        ('Permissions ',{'fields':['is_active','is_superuser','is_staff']}),
        ('Privacy',{'fields':['search','suggest']})
    ]

    # Fields for adding a user in the admin
    add_fieldsets = [
        ('User Credentials', {
            'fields': ['email', 'password1', 'password2'],
        }),
    ]

    search_fields = ['email']
    ordering = ["email","id"]
    filter_horizontal = []

admin.site.register(User , UserModelAdmin) 

@admin.register(FreindRequest)
class RequestsModel(admin.ModelAdmin):
    list_display = ['id','sender','rece','status','timestamp','room_no'] 


@admin.register(Message)
class Messages(admin.ModelAdmin):
    list_display = ['id','send_msg','rece_msg','message','timestamp','is_read']

@admin.register(Themes)
class Themes(admin.ModelAdmin):
    list_display = ['id','user','font','size','color_rece','color_send','bg1','bg2','border']

    fieldsets = [
        
        ('User',{'fields':['user']}),
        ('Font & Size',{'fields':['font','size']}),
        ('Color & Background',{'fields':['color_rece','color_send','bg1','bg2','border']}),
    ]