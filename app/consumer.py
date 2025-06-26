from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer as SC
from channels.exceptions import StopConsumer
import json 
from random import randint
from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync , sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model 
from .models import Message 
from django.db.models import Q 

 
channel_layer = get_channel_layer()
count = []
cond = False
user_dict = {}
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        global user_dict
        global count 
        global cond
        print("yes Connected")

        print("Channel Name : ",self.channel_name)
        self.group_name = str(self.scope['url_route']['kwargs']['group_no']).replace("\"","")
        self.username = self.scope['session'].get('username','Anonymous')

        print("THIS IS USERNAME OF USER :" , self.username)
        

        if self.group_name not in user_dict:
            user_dict[self.group_name] = {'sender':{},'receiver':{}}


        if len(user_dict[self.group_name]['sender']) == 0:
            user_dict[self.group_name]['sender']['channel_name'] = self.channel_name
        else : 
            user_dict[self.group_name]['receiver']['channel_name'] = self.channel_name

        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.send({
            'type':"websocket.accept"

        })
    

        print("The value of count is  : ",count)

        if self.group_name in count: 
            for i in count:
                if i is self.group_name: 
                    count.remove(i) 
            
            #async_to_sync(channel_layer.group_send)(self.group_name,{'type':'websocket.msgs','message' : json.dumps({'msg':'.^aconnected.^a'})})

        else:
            count.append(self.group_name)

    def msg_direct_send(self,event):
        print("I AM RUNNING , AND I AM MSG_DIRECT_SEND !",event) 
        self.send({
            'type':'websocket.send',
            'text': json.dumps(event)
         }
        )  
    


    def websocket_receive(self,event): 
        global user_dict
 
        if 'username' not in user_dict[self.group_name]['sender']:
            user_dict[self.group_name]['sender']['username'] = (json.loads(event['text']))['username']
        elif 'username' not in user_dict[self.group_name]['receiver']:
            user_dict[self.group_name]['receiver']['username'] = (json.loads(event['text']))['username']
        
        if 'username' in user_dict[self.group_name]['sender'] and 'username' in user_dict[self.group_name]['receiver']:
            async_to_sync(channel_layer.send)(user_dict[self.group_name]['receiver'].get('channel_name'),{'type':'msg_direct_send','username':user_dict[self.group_name]['sender']['username']})
            async_to_sync(channel_layer.send)(user_dict[self.group_name]['sender'].get('channel_name'),{'type':'msg_direct_send','username':user_dict[self.group_name]['receiver']['username']})
        print("This is Dict : ",user_dict) 

        # if len(user_dict[self.group_name]) == 2: 
        #     current_username = user_dict[self.group_name][self.channel_name]
        #     self.send('type':'websocket.send',
        #         'message' : json.dumps({
        #         'type': 'user_info',
        #         'current_user': current_username,  # Current user's username
        #         'all_users': user_dict[self.group_name]  # All connected users in the group
        #     }))
        
        # if self.scope['user'].is_authenticated:
            
        # data = json.loads(event['text'])
        # chat = Chat(content=data['msg'],group=group) 
        # chat.save() 
        # data['user'] = self.scope['user'].username
        # print("this is the actual data : ",data)            
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'websocket.msgs',
                'message' : event['text']
            })
            
        # else:
            
        #     self.send({
        #         "type": "websocket.send",
        #         "text": json.dumps({'msg':"Login Require"})
        #         })
        
    def websocket_msgs(self,event):
        print("This is the actual event : ",event['message'])
        
        self.send({
            'type':'websocket.send',
            'text': event['message']
        }
        )         
      
    def websocket_disconnect(self,event):
        print("Yes Disconnected")
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        raise StopConsumer


queue_elements = []
class RandomChatSync(SC):
    def add_to_queue(self,channel_name):
        global queue_elements
        queue_elements.append(str(channel_name))
        # async_to_sync(channel_layer.group_add)("queue_chat",channel_name)
        # print("THIS IS CHANNEL NAME : ",self.channel_name)

    def connect_random(self,channel_name):
        global queue_elements 
        if len(queue_elements) > 1:
            queue_elements.remove(channel_name)
            matched_channel = queue_elements[0] 
            queue_elements.remove(matched_channel) 
            self.chat_no = f"chat_{randint(100000, 999999)}"
            return matched_channel , self.chat_no 
        return None , None 

    def connect(self):
        print("Websocket Connect")
        self.accept() 
        self.add_to_queue(self.channel_name)
        # self.chat_no = None 
        matched , chat_no = self.connect_random(self.channel_name)
        if chat_no: 
            # chat_no = str(chat_no)
            self.chat_no = chat_no 
            async_to_sync(channel_layer.group_add)(self.chat_no,self.channel_name)
            async_to_sync(channel_layer.group_add)(self.chat_no,matched)
            async_to_sync(channel_layer.group_send)(self.chat_no,{'type':'message_send','message' : {'msg':'.^aconnected.^a','chat_no':chat_no}})
            print("Chat No : ",self.chat_no) 
        # else:
            # self.send(text_data="Waiting for other user ... ")


    def receive(self,text_data):
        print('The text data is  :',text_data)  
        data = json.loads(text_data)
        print("MEssage" ,data)
        async_to_sync(channel_layer.group_send)(data['chat_no'],{
            'type':'message_send',
            'message' : data
        })


    def message_send(self,event):
        print("This is event : ",type(event)) 
        self.send(json.dumps(event['message']))  

    def disconnect(self,event):
        print("disconenct")      
        raise StopConsumer   
    


User = get_user_model() 
class LoginChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['friend_username'] 
        print("the group name is :",self.group_name)
        li = str(self.group_name).replace("0","1") 
        li = list(str(li).replace("-",""))
        li = li[1:len(li)-1]
        print(li)
        val = [chr(int(num)+64) for num in li]
        self.room_name = "".join(val)

        print("this value is : ",self.room_name)
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            print("YES CODE WAS WORKING DONT WORRY ###### room name : " , self.room_name)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept() 

            # **STEP 1: Send Unread Messages**

            unread_messages = await sync_to_async(lambda : list(Message.objects.filter(rece_msg=self.user, is_read=False)))()
            # print(unread_messages)
            # # unread_messages = {'fullname':"Sandeep"}
            if unread_messages:
                for msg in unread_messages:
                    msg.is_read = True 
                    await sync_to_async(msg.save)()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data) 
        if data.get('dblclk'):
            print("Yes data access")
            mail = str(data['U2']).replace('"',"")
            print("mail is : ",mail)  
            Uone = await sync_to_async(lambda :User.objects.get(fullname = data['U1']).id)()
            Utwo = await sync_to_async(lambda :User.objects.get(fullname = mail).id)() 
            print("THE USERIDS : ",Uone)
            print("THE USERIDS : ",Utwo) 
            data = await sync_to_async(lambda :Message.objects.filter(Q(Q(Q(send_msg=Uone) & Q(rece_msg=Utwo)) | Q(Q(send_msg=Utwo) &Q(rece_msg=Uone))), message=data['msg']).delete() )()
            await sync_to_async(print)("The data is : ",data) 
            await self.chat_message({'room_nos': self.room_name, 'msg': 'reload1this1page'})
            return 
        
        if data['room_no'] == '...': 
            try:
                await self.chat_message({'room_no': self.room_name, 'msg': '.^aconnected.^a'})
                receiver_username = str(data["receiver"]).strip('"')  # Clean receiver username

                receiver_usernames = await sync_to_async(lambda :User.objects.filter(email=receiver_username).first(),thread_sensitive=True)()
                old_chat = await sync_to_async(
                    lambda: list(
                        Message.objects.filter(send_msg=self.user, rece_msg=receiver_usernames)
                        .union(Message.objects.filter(send_msg=receiver_usernames, rece_msg=self.user))
                        .order_by("timestamp")
                    ),
                    thread_sensitive=True
                )()
                await sync_to_async(print)(old_chat)  
                for i in old_chat:
                    await self.chat_message(
                        {
                        "type":"chat_message",
                        "sender": await sync_to_async(lambda : (User.objects.get(email = i.send_msg).fullname))(),
                        "msg": i.message,
                        "receiver": await sync_to_async(lambda :(User.objects.get(email=i.rece_msg).fullname))(),
                        "timestamp": i.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "seen": i.is_read
                        }
                    )
    
            except Exception as e:
                print("Error is : ",e)
                return 
            return
        else:
            print("This is test data in ML :",text_data) 
            sender = self.user
            print("UNREAD MESSAGES : ", data, sender)
            receiver_username = str(data["receiver"]).replace('"',"")
            message = data["msg"]

            try:
                print("This is a receiver : ",str(receiver_username).replace(' ',""))
                receiver = await sync_to_async(User.objects.get)(email=str(receiver_username).replace(' ',""))
            except User.DoesNotExist:
                print("This is a receivers : ")
                return

            # **STEP 2: Store Message in Database**

            msg = await sync_to_async(Message.objects.create)(send_msg=sender, rece_msg=receiver, message=message)

            # **STEP 3: Send Message in Real-time if Receiver is Online**
            await self.channel_layer.group_send(
                data['room_no'],
                {
                    "type": "chat_message",
                    "sender": sender.fullname,
                    "msg": message,
                    "timestamp": str(msg.timestamp),
                }
            )



    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

