from django.shortcuts import render,HttpResponse,redirect
from .models import Room,Topic,Message,photo
from .forms import RoomForm,MessageForm,UserForm,PhotoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required # for login is required for creating rooms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    # rooms=[
    # {'id':1,'name':'Python geeks'},
    # {'id':2,'name':'Lets C'},
    # {'id':3,'name':'Frontend masters'}
    # ]
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                               Q(name__icontains=q) |
                               Q(description__icontains=q)) 
    topics = Topic.objects.all()[:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.all()


    return render(request,'main.html',{'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages })

@login_required(login_url='login')
def rooms(request,pk):

    if request.user.is_authenticated: 
        room =Room.objects.get(id=pk)     
        participants = room.participants.all()
        room_messages = room.message_set.all()

        '''if request.method=="POST":
            print('this code is running')
            message_body = request.POST.get('body') 
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = message_body
            )
            room.participants.add(request.user)
            context = {
                'user':request.user,
                'message':message,
                
            }
            print(f'message body : {message_body}')
            return render(request,'chat_messages_partial.html',context)'''
            
        return render(request,'rooms.html',{'room':room,'pk':pk,'room_messages':room_messages,'participants':participants})
    return redirect('/login')


@login_required(login_url='login')
def createroom(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    # if True:
    # form = RoomForm(request.POST)
    topics = Topic.objects.all()


    if request.method=='POST':
        room_name = request.POST.get('room_name')
        # topic_name = request.POST.get('dropdown')
        topic = Topic.objects.get(name=request.POST.get('dropdown'))
        room_about = request.POST.get('room_about')
        form = RoomForm(data={

            'host':request.user,
            'name':room_name,
            'topic':topic,
            'description':room_about
        })
        print(request.user,room_name,topic,room_about,sep='\n')
        if form.is_valid() :
            form.save()
            messages.success(request,'Room created successfully!')
            

            # return redirect(f'/rooms/{room.id}')
        else:
            messages.error(request,'Something wrong happened!')
        return redirect('/')

    return render(request,'createroom.html',{'topics':topics})
@login_required(login_url='login')
def updateroom(request,pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user!=room.host and not request.user.is_superuser :
        messages.error(request,'You are not authenticated to perform the operation!!')
        return redirect('/')
    if request.method == 'POST':
        room_name = request.POST.get("room_name")
        room_about = request.POST.get("room_about")
        room_topic = Topic.objects.get(name=request.POST.get("dropdown"))
        form = RoomForm(data={
            'host':request.user,
            'name':room_name,
            'description':room_about,
            'topic':room_topic,
        },instance=room)

        if form.is_valid():
            form.save()
            return redirect(f"/rooms/{pk}")
        messages.error(request,"Something went wrong while updating the details!")
        return redirect("/")


    return render(request,'updateroom.html',{'form':form,'pk':pk,'room':room,'topics':topics})

def deleteroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request,'delete.html',{'obj':room,'pk':pk})



def Userlogin(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('/')
    username=  request.POST.get('username')
    password1 = request.POST.get('password')
    if request.method=='POST':
        
        user = authenticate(request,username=username,password=password1)

        if user is not None:
            login(request,user)
            return redirect('/')

        else:
            messages.error(request,'User does not exists!')
            print('Something went wrong!!, user=',user)
        return redirect('/login')
    return render(request,'login.html',{'page':page})

@login_required(login_url='login')
def Userlogout(request):
    logout(request)
    return redirect('/')

def Userregister(request):
    if request.user.is_authenticated :
        return redirect('/')
    page = 'register'
    form = UserForm()
    if request.method == 'POST':
        
        
        form = UserForm(
            data={
            "first_name" : request.POST.get('firstname'),
            "last_name":request.POST.get('lastname'),
            "username":request.POST.get('username'),
            "password":request.POST.get('password'),
            "email":request.POST.get('email')

        }
        )
        print(request.POST.get('password'))
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.username = user.username.strip()
            user.set_password(request.POST.get('password'))
            user.save()
            login(request,user)
            print('user form is valid')
            return redirect('/')
        messages.error(request,'Something went wrong!')
        return render(request,'login.html')

    return render(request,'login.html',{'page':page,'form':form})
@login_required(login_url='login')
def edit_message(request,pk1,pk2):
    message = Message.objects.get(id=pk2)
    if message.user != request.user :
        return HttpResponse('Nahi hoga edit chal bhaag yahan see!!')
    form = MessageForm(instance=message)
    
    if request.method=='POST':
        form = MessageForm(request.POST,instance=message)
        if form.is_valid():
            form.save()
            return redirect(f'/rooms/{pk1}')
    return render(request,'edit-message.html',{'form':form,'pk1':pk1,'pk2':pk2})

@login_required(login_url='login')
def delete_message(request,pk1,pk2):
    
    message = Message.objects.get(id = pk2)
    if request.user == message.user or request.user.is_superuser:
        message.delete()
        return redirect(request.META.get('HTTP_REFERER','default-view'))
    return redirect(f'/rooms/{pk1}')
# def edit_message(request,pk1,pk2):
#     return HttpResponse('Edit your message here')

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    room_messages = Message.objects.filter(user__id=pk)[:5]
    topics = Topic.objects.all()[:5]
    user_rooms = Room.objects.filter(host = user)

    

    return render(request,'userProfile.html',{'user':user,'room_messages':room_messages,'topics':topics,'user_rooms':user_rooms})

@login_required(login_url='login')
def topics(request):
    topics = Topic.objects.all()
    return render(request,'topics.html',{"topics":topics})

@login_required(login_url='login')
def activity(request):
    return render(request,'activity.html')

@login_required(login_url='login')
def editUser(request,pk):

    user1 = User.objects.get(id=pk)
    if request.user != user1 and not request.user.is_superuser:
        return redirect('/')
    else:

        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            date_joined = user1.date_joined
            user_bio = request.POST.get("user_bio")
            anyUser = UserChangeForm(data={
                "username":username,
                "email":email,
                "date_joined":date_joined,
                "is_active":request.user.is_active,
                "is_staff":request.user.is_staff,
                "is_superuser":request.user.is_superuser,

            },instance = user1)

            image = request.FILES.get('image')
            photo_rec = photo.objects.get(user=user1)
            form = PhotoForm(data={
                "user":user1   
            },
            files ={
                "image":image
            },
            instance=photo_rec
            
            )
            if form.is_valid():
                form.save()
                print('image form is valid',f'user-name: {request.user.username}')
            else:
                print(form.errors)
            if anyUser.is_valid():
                
                anyUser.save()
                print("userform is valid")
                return redirect(f"Profile/{user1.id}")
            else :
                messages.error(request,"Something went wrong!") 
                print(anyUser.errors)
                return redirect("/")
        
    return render(request,'edit-user.html',{"user":user1})


def get_photos(request):
    photo_rec = photo.objects.get(user = request.user)
    return render(request,'photo.html',{'photo':photo_rec})