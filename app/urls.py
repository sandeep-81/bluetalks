from django.urls import path 
from . import views 


urlpatterns = [
    path("",views.home,name="home"),
    path("home/",views.home,name="home"),
    # path("<str:group_name>/",views.index),
    path("randchat/",views.randomchat), 
    path("chat/<str:group_no>/",views.chat),
    path("generatecode/",views.generatecode),
    path("verify/",views.verify_code , name="verify-code"), 
    path("about/",views.about),
    path("login/",views.login,name="login"),
    path("login/home/",views.home,name="home"),
    path('logout/',views.logout , name='logout'),  
    path("register/",views.register,name="register"),
    path("login/forgetp/",views.forget_pass),
    path("login/forgetp/changepwd/",views.changepass),
    path("register/regsiter_otp/",views.registerotp),
    path('user/',views.user_screen , name="user"),
    path('login_user_screen/',views.login_user_screen , name="login_user_screen"),
    path('friends/',views.friends , name="friends"), 
    path('user/<str:friend_username>/',views.get_messages , name="get_messages"), 
    # path("user/", views.special_user, name="special_user"),  
    path("account/", views.account_sett, name="account_sett"),  
    path("themes/", views.themes, name="themes"),  
 

]

