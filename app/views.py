from django.shortcuts import render , redirect
from .models import User as User , FreindRequest , Message , Themes
from random import randint 
from email.message import EmailMessage 
import smtplib  
from django.db.models import Q 
from django.contrib import messages 
from django.contrib.auth import login as auth_login ,logout as auth_logout ,authenticate 
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.contrib.auth import get_user_model 


group_no = 0 
otp = 0
email = ""
count = 0
total_user = 0
username = ""
usernames_dict = {'generater':"generator",'filler':'filler','genuser':'user','filluser':'user'} 

def common_context(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(email=request.user.email)
            return {
                'fullname': user.fullname,
                'email': user.email
            }
        except User.DoesNotExist:
            pass 

    return {
        'fullname': None,
        'email': None
    }

def index(request):
    # This is called ORM Operation (object-relationship mapper)
    # filter_group = Group.objects.filter(name = group_name).first() 
    # chat = []
    # if filter_group:
    #     chat = Chat.objects.filter(group = filter_group)
    # else : 
    #     group_add  = Group(name = group_name)
    #     group_add.save()

    # print("Filter Group Name :",filter_group)
    return render(request,"chat.html")

def home(request):
    global username 
    if request.method == "POST":
        username = request.POST.get('username') 
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        country = request.POST.get("country")
        print(username , gender , age , country)
        return redirect("/generatecode/") 

    return render(request,"home.html")

def generatecode(request):
    global total_user
    global usernames_dict
    global username
    rand = "Generate"
    global group_no
    if request.method == "POST":
        rand = randint(100000,999999)
        group_no = rand
        if total_user > 2:
            total_user = 0
        total_user += 1
        usernames_dict['generater'] = username
        usernames_dict['genuser'] = 'generater'
    print("The value of the random number : ",rand)
    return render(request,"generatecode.html",{'rand':rand})
    

def chat(request , group_no):
    global usernames_dict
    global count 
    global total_user
    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password")
        return login_additional(request , email , password)

    print("The count is in which views : ",count)
    # count += 1 
    print(group_no , username , count , usernames_dict['generater'] , usernames_dict['filler'] , total_user)
    return render(request, "chat.html",{'group_no':group_no , 'username':username ,'member': count , 'generater':usernames_dict['generater'] ,'filler': usernames_dict['filler'] ,'filluser':usernames_dict['filluser'],'genuser':usernames_dict['genuser'], 'total_user': total_user})

def verify_code(request):
    global usernames_dict
    global total_user
    global username 
    if request.method == "POST":
        user_code = request.POST.get("code")
        print(f"User Code : {type(user_code)} | Group Code : {type(group_no)}")
        if str(user_code) == str(group_no):
            usernames_dict['filler'] = username
            usernames_dict['filluser'] = 'filler'
            total_user += 1
            return redirect(f'/chat/{group_no}/') 
        else:  
            return render(request,"generatecode.html",{'rand':"Generate"})
        
def about(request):
    return render(request , "about.html")

def login(request ,val=0):
    if val == 0:
        if request.method == "POST":
            email = request.POST.get("email") 
            password = request.POST.get("password")
            return login_additional(request , email , password)

    return render(request , "login.html")

def login_additional(request , email , password):
        user = authenticate(request, email=email, password=password) 
        print("THE USER IS :- ",user)
        # user = User.objects.get(email = email)
        # if user.check_password(password):
        if user is not None:
            auth_login(request,user)
            print("This is user.is_authenticated :- ",user.is_authenticated)
            print("LOGIN") 
            messages.add_message(request, messages.SUCCESS, "Login Sucessful !")
            return redirect('login_user_screen')  
            #return render(request,"home.html") 
        else: 
            print(" No LOGIN",user)  
            # messages.add_message(request, messages.ERROR, "Invalid Email and Password !")
            messages.error(request, "Invalid Email and Password !")
            # return login(request,val=1) 
        return render(request , "login.html",{'error':'yes'})


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        global otp
        global user_details
        user_details = {'username':name , 'email':email,'password':password}
        otp = randint(100000,999999)
        print("Name : ",name ,"\nEmail : ",email,"\nPassword : ",password)
        subject = f"Verify Your Account - BlueTalks"
        content = f"""
Hi {name},
Thank you for registering with BlueTalks! To complete your registration, please verify your email address by entering the OTP below:
**Your OTP is: {otp}**
This OTP is valid for the next 15 minutes. Please do not share this code with anyone.
If you did not request this verification, please ignore this email.
Best regards,  
The BlueTalks Team
""" 
        
        send_email(subject , content , email)
        # return render(request , "register_otp.html")
        if send_email:
            return redirect("regsiter_otp/")
            # return render(request ,"register_otp.html")

    return render(request , "register.html")
                  
def registerotp(request):
    global otp
    print("YES I AM WORKING NOW ! ")
    if request.method == "POST":
        fetch_otp = request.POST.get("otp")
        print("Fetch OTP :",fetch_otp, type(fetch_otp) ,"\nOrignal OTP : ",otp , type(otp))
        if str(otp) == str(fetch_otp):
            print("Sucessfully OTP Match")
            user = User.objects.create_user(email = user_details['email'] ,fullname = user_details['username'] , password= user_details['password'])
            # theme = Themes.objects.create(user = user_details['email'])   
            messages.add_message(request, messages.SUCCESS,"Registeration Successfull")
            otp = 0
            return redirect('login')
        else :
            messages.add_message(request, messages.ERROR, "Invalid OTP")

    return render(request , "register_otp.html")
    

def changepass(request):
    global email
    if request.method == "POST":
        pwd = request.POST.get("password")
        cpwd = request.POST.get("cpassword")
        if pwd == cpwd :
            user = User.objects.get(email = email)
            user.set_password(pwd)
            user.save()
            email = ""
            messages.add_message(request , messages.INFO,"Your password has been successfully changed..")
            return render(request , "login.html") 
        else:
            messages.add_message(request , messages.ERROR,"Password does not match. Please try again.")

    return render(request , "change_pass.html")

def forget_pass(request):
    global otp
    global email
    print("YES I AM WORKING BOSS !") 
    if request.method == "POST" and otp != 0:
        fetch_otp = request.POST.get("otp")
        print("This OTP you enter in box : ",fetch_otp)
        if str(fetch_otp) != str(otp):
            messages.add_message(request , messages.ERROR , "Invalid OTP. Please try again. !")
        else:
            otp = 0
            return redirect("changepwd/")

    
    if request.method == "POST":
        email = request.POST.get("email")
        user  = User.objects.filter(email = email).first()
        if user:
            print("Email : ",email)
            otp = randint(100000,999999)
            subject = "Password Reset Request for Your Account"
            content = f"""
Dear User,
We received a request to reset the password for your account. 
Your OTP (One-Time Password) is: {otp}
Please use this OTP within the next 10 minutes to reset your password. If you did not request this, please ignore this email. Your account remains secure.
Thank you,  
The BlueTalks Team
"""
            send_email(subject, content , email)
        else:
            messages.add_message(request , messages.ERROR , "Invalid Email !")
    return render(request , "forget_pass.html",{'email':email , "otp":otp})



def send_email(subject, body, to_email):
    # Create an EmailMessage object
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = 'bluetalksapp@gmail.com'  # Replace with your sender email
        msg['To'] = to_email
        msg.set_content(body)

        # Connect to the Gmail SMTP server using smtplib
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                # Use your actual Gmail credentials here
                smtp.login('Bluetalksapp', 'urob hogr jlmd kzqw')  # Replace with your Gmail password
                smtp.send_message(msg)

            print('Email sent successfully!')
            return True
        except Exception as e:
            print(f"Error: {e}")
            

def logout(request): 
    auth_logout(request)
    return render(request,"home.html") 

def randomchat(request ): 
    print("Yes access") 
    return render(request ,"randomchat.html")

@login_required
def chat_friend_list(request):
    if request.method == "POST":
        if request.POST.get("ori-msg"):
            print("ORIGNAL MESSAGE : ",request.POST.get("ori-msg"))
    friends = all_friend_fn(request.user)
    print("My Friends : ",friends)
    friends_li =[]
    for i in friends:

        user_mail = User.objects.filter(fullname=i["fullname"]).first()        

        mail = User.objects.get(email = str( Message.objects.filter((Q(send_msg = request.user) | Q(rece_msg = request.user)) and (Q(send_msg = user_mail) | Q(rece_msg = (user_mail)))).order_by("-timestamp").first().send_msg)).fullname 
        if str(mail) == str(User.objects.get(email = request.user).fullname): 
            mail = str("You") 

        print("The user namil is = ",user_mail)

        serious = Message.objects.filter((Q(send_msg = request.user) | Q(rece_msg = request.user)) and (Q(send_msg = user_mail) | Q(rece_msg = (user_mail)))).order_by("-timestamp").first()

        friends_li.append([i['fullname'],
                            mail,
                            serious.message,
                            i['room_no']]
                            )
        print("the I value is : ",friends_li )
        friends_li.reverse()
        print("the I value is Reverse : ",friends_li ) 
        
    return friends_li
        
def user_screen(request):
    ###################################################################################################################################
    search =""
    filter_names = ""
    context = {}
    if request.method == "GET":
            if request.GET.get("search"):
                search = request.GET.get("search")
                print("Search is :",search)
                filter_names = find_friend(request,search) 
                print("Filter name  is :",filter_names)
            


    context['filter_name'] = filter_names
    context["value"] = search
    context["mail"] = request.user
    ###################################################################################################################################

    friends_li = ""
    try:
        if Message.objects.filter(Q(send_msg=request.user) | Q(rece_msg=request.user)).values_list('send_msg__email', 'rece_msg__email'):
            friends_li = chat_friend_list(request)
            print("Yahoo Friend List : ",friends_li) 
             
    except Exception as e:
        print("Error is : ",e) 
        friends_li = []
    # friends_li = chat_friend_list(request)
    context['sample'] = friends_li
    context['current_user'] = "..."
    print("This is context : ",context)

    return render(request , "user.html",context) 


@login_required
def login_user_screen(request):
    if Themes.objects.filter(user = request.user).exists():
        pass
    else:
        Themes.objects.create(user = request.user) 

    if request.method == "GET":
        print("YES WORKED 1")
        if request.GET.get("username_f"):
            print("YES WORKED 2")
            f_username = request.GET.get("username_f") 
            friend_username_find(f_username,request.user)
        if request.GET.get("search"):
            search = request.GET.get("search")
            print("THIS IS SEARCHED DATA : ",search) 
            filter_names = find_friend(request,search) 
            print("THIS IS Filter name DATA : ",filter_names)  

            return render(request,"login_user_screen.html",{'filter_name':filter_names,"value":search,"mail":request.user})  
    return render(request,"login_user_screen.html") 

@login_required
def friends(request):
    search =""
    filter_names = ""
    if request.method == "GET":
        if request.GET.get("hidden"):
            sender_mail = User.objects.get(fullname = request.GET.get("hidden")).email
            sender_user = User.objects.get(email=sender_mail) 
            update_data = FreindRequest.objects.filter(sender = sender_user).update(status = "Friend")
            print('This is Good Thing : ',update_data)

        if request.GET.get("search"):
            search = request.GET.get("search")
            filter_names = find_friend(request,search) 

            # return render(request,"login_user_screen.html",{'filter_name':filter_names,"value":search,"mail":request.user})
            
    if request.method == "POST":
        if request.POST.get("gotochat"):
            print("THIS IS CHAT NOT MORE : ",request.POST.get("gotochat"))
            return render(request , "user.html",{'sample':['Aman','Shant','Navjot','Dishu','Aman','Shant','Navjot','Dishu','Aman','Shant','Navjot','Dishu'],"current":request.POST.get("gotochat")}) 

            # return redirect("special_user")
            
            
            ################################################################################## Yaha add karna hai 
    friends = all_friend_fn(request.user)
    friends.reverse()
    context = {'request_list':[],'friend':friends,"mail":request.user}
    request_get = FreindRequest.objects.filter(rece = request.user,status="Request")
    for req in request_get:
        req_gets = req.sender
        sender = User.objects.get(email = str(req_gets)).fullname  
        print("Sender : ",sender)
        room_no = list(FreindRequest.objects.filter(rece = request.user,status="Request").all())
        context['request_list'].append(sender)
    context['request_list'].reverse()

    context['filter_name'] = filter_names
    context["value"] = search
    context["mail"] = request.user
    print("Context is : ",context)
    return render(request , "friends.html",context)  

# def special_user(request):
#     data_dict = request.session.pop("data_dict", None)  # Data fetch karne ke baad remove kar diya
#     return render(request, "user.html", {"data": data_dict})

def find_friend(request,name):
    li = {
        'request':[],
        'friends':[],
        'unknown':[],
    }
    print("YES WORKS ....................................... ") 
    # search_friend = User.objects.filter(fullname = name).first()
    search_friend = User.objects.exclude(Q(email = request.user) | Q(email = "admin@gmail.com") |Q(search = False)).values_list("fullname",flat=True)
    print("THIS IS RESULT OF THE 301 :- ",type(User.objects.filter(email = request.user).values_list('fullname',flat=True)))
    print("Search Friend is  :- ",search_friend)
    for find in search_friend:
        mail_user = User.objects.get(fullname = find).id                       
        print("MAIL USER : ",type(mail_user),mail_user,"\nREQUEST USER : ",type(request.user),request.user )
        a = FreindRequest.objects.filter((Q(sender = request.user) | Q(rece = request.user)) & (Q(rece = mail_user) | Q(sender = mail_user)) & Q(status = "Friend")).values_list('rece',flat=True)
        # a = FreindRequest.objects.filter(rece = mail_user).first()
        print("VALUE OF A IS : ",a)
        if FreindRequest.objects.filter(sender = request.user).first() and FreindRequest.objects.filter(rece = mail_user).first() and FreindRequest.objects.filter(status = "Request").first():
                li['request'].append(find)
        elif FreindRequest.objects.filter(Q(Q(Q(sender = request.user) | Q(rece = request.user)) & (Q(rece = mail_user) | Q(sender = mail_user))) & Q(status = "Friend")).first():
            print("YES FRIEND IS HERE ...... ",name , find)  
            if str(name).lower() in str(find).lower(): 
                li['friends'].append(find)
        else:
            print("Try by IF condition : ",find)
            if str(name).lower() in str(find).lower(): 
                li['unknown'].append(str(find)) 

    print(li) 
    
    return li   

def friend_username_find(rece,send):
    find = User.objects.get(fullname = rece)
    uploadRequest = FreindRequest(sender = send,rece = find,status = "Request")
    uploadRequest.save()
    print(FreindRequest.objects.all().values_list())

def all_friend_fn(mail):
    print(mail)
    sender_s = FreindRequest.objects.filter(sender = mail ,status = "Friend").select_related("rece")
    recever_r = FreindRequest.objects.filter(rece = mail, status = "Friend").select_related("sender")
    
    print("Friends list:", sender_s , recever_r) 
    all_friend = [{'fullname':friend.rece.fullname , 'room_no':friend.room_no} for friend in sender_s] + [{'fullname':friend.sender.fullname , 'room_no':friend.room_no} for friend in recever_r]
    print("Friends:", all_friend )
    return all_friend



@api_view(["GET","POST"]) 
def get_messages(request,friend_username): 
    print("FRIEND USERNAME : ",friend_username)


    one_id = str(friend_username).split("-")[0] 
    two_id = str(friend_username).split("-")[1] 
    user1 = User.objects.get(id = one_id)
    user2 = User.objects.get(id = two_id) 
    print("ID one : ",user1 ,"\nID Two : ", user2)  
    friends_li = ""
    # friends_li = chat_friend_list(request) 
    try:
        if Message.objects.filter(Q(send_msg=request.user) | Q(rece_msg=request.user)).values_list('send_msg__email', 'rece_msg__email'):
            friends_li = chat_friend_list(request)
             
    except Exception as e:
        print("Error is : ",e) 
        friends_li = []
    print("This is friend list is offical launch by google : ",friends_li)

    if request.method == "POST":
        # Find the friend in the database
        t = Themes.objects.get(user = request.user)
        theme_list = [t.user , t.font , t.size , t.color_rece , t.color_send , t.bg1 ,t.bg2 , t.border,""] 
        theme_list = str(theme_list) 
        print("Theme List is  :" ,theme_list)

        if str(request.user) == str(user1.email):
            friend = get_user_model().objects.filter(fullname__iexact=user2.fullname).first()
            print("this is me 1 : ",request.user)
            print("is this your friend 1 : ",friend)
            return render(request , "user.html",{'username':str(friend),
                                                 'current_user':User.objects.get(email = str(friend)).fullname,
                                                 'friend_username': friend_username ,
                                                 'sample': friends_li,
                                                 'theme':theme_list}
                                                )


        elif str(request.user) == str(user2.email): 
            friend = get_user_model().objects.filter(fullname__iexact=user1.fullname).first()
            print("this is me 2 : ",request.user)
            print("is this your friend 2 : ",friend)
            return render(request , "user.html",{'username':str(friend),
                                                 'current_user':User.objects.get(email = str(friend)).fullname , 
                                                 'friend_username': friend_username,
                                                 'sample': friends_li,
                                                 'theme':theme_list
                                                    }
                                                 )    
        else:
            return Response({"error": "User not found"}, status=404)

        # print(f"YES CODE IS WORKING: Found Friend -> {friend}")

        # # Fetch chat messages (both sent and received)
        # messages = Message.objects.filter(
        #     send_msg__in=[user, friend], 
        #     rece_msg__in=[user, friend]
        # ).order_by("timestamp")  # Now timestamp exists

        # messages_list = [
        #     {
        #         "send_msg": msg.send_msg.fullname,  # Corrected field
        #         "rece_msg": msg.rece_msg.fullname,  # Corrected field
        #         "message": msg.message,
        #         "timestamp": str(msg.timestamp),
        #         "is_read": msg.is_read
        #     }
        #     for msg in messages
        # ]
        # print("The friend name is : ",friend)


    # elif request.method == "POST":
    #         data = request.data
    #         print("POST METHOD DOWN WALA .......................... ")
    #         print("This is request user 2 : ",request.user)

    #         if one_id != User.objects.get(email = request.user).id:
    #             user_id_found = User.objects.get(id = one_id).fullname 
    #             friend = get_user_model().objects.filter(fullname__iexact=user_id_found).first()
    #         else: 
    #             user_id_found = User.objects.get(id = two_id).fullname 
    #             friend = get_user_model().objects.filter(fullname__iexact=user_id_found).first()
    #         if not friend:               
    #             return Response({"error": "User not found"}, status=404)

    #         message = data.get("message", "").strip()
    #         if not message:
    #             return Response({"error": "Message cannot be empty"}, status=400)

    #         # Save message
    #         new_message = Message.objects.create(
    #             send_msg=user,
    #             rece_msg=friend,
    #             message=message
    #         )
    #         print("The friend name is : ",friend)
    #         return Response({
    #             "message": "Message sent successfully",
    #             "message_id": new_message.id
    #         }, status=201)


def account_sett(request):
    print(request)
    user = User.objects.get(email = request.user) 
    print("The data is : ",user) 
    address = []
    privacy = [] 
    if user.country == "-":
        country = ""
        address.append(country)
    else:
        country = user.country
        address.append(country)
    if user.state == "-": 
        state = ""
        address.append(state)
    else:
        state = user.state
        address.append(state)
    if user.distt == "-":
        distt = ""
        address.append(distt)
    else:
        distt = user.distt
        address.append(distt)
    if user.pincode== "-":
        pincode = ""
        address.append(pincode)
    else:
        pincode = user.pincode
        address.append(pincode)

    if user.search == True:
        privacy.append("Checked")
    else:
        privacy.append("")

    if user.suggest == True:
        privacy.append("Checked")
    else:
        privacy.append("")

    if request.method == "POST":
        if request.POST.get("fullname"):
            user_data = User.objects.get(email = request.user)

            user_data.fullname = request.POST.get("fullname")
            user_data.about = request.POST.get("about")
            user_data.country = request.POST.get("country")
            user_data.state= request.POST.get("state")
            user_data.distt = request.POST.get("distt")
            user_data.pincode = request.POST.get("pincode")
            if request.POST.get("search") == None:
                user_data.search = False
            else:
                user_data.search = True

            if request.POST.get("suggest") == None:
                user_data.suggest = False
            else:
                user_data.suggest = True 

            print("SEARCHED : ",request.POST.get("search"))
            print("SUGGESTED : ",request.POST.get("suggest"))
            user_data.save()
            return redirect('account_sett') 
        
    print("USER ABOUT : : : ",user.about)
    
    return render(request,"acc_setting.html",{"email":user.email , "fullname":user.fullname,"about":user.about,"address":address,'privacy':privacy}) 

def themes(request):
        t = Themes.objects.get(user = request.user)
        theme_list = [t.user , t.font , t.size , t.color_rece , t.color_send , t.bg1 ,t.bg2 , t.border,""] 
        if request.method == "POST":
            if request.POST.get("font"):
                d = Themes.objects.get(user = request.user)
                d.font = request.POST.get("font")
                d.size = request.POST.get("size")
                d.color_rece = request.POST.get("color_rec")
                d.color_send = request.POST.get("color_send")
                d.bg1 = request.POST.get("bg1")
                d.bg2 = request.POST.get("bg2")
                d.border = request.POST.get("border")
                d.save()
                return redirect("themes")
                
        return render(request,"themes.html" , {'theme':theme_list})