from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import UserInfo, ChatRoom, Message


# Create your views here.
def register(request) :
    if request.method  ==  'POST' :
        username =  request.POST['username']
        password =  request.POST['password']
        name  =  request.POST['name']
        email = request.POST['email']
        image  = request.FILES.get('image')

        if User.objects.filter(username = username).exists()  :
            messages.error(request , "Username already taken")
            return redirect('register')

        user  =  User.objects.create_user(username= username ,  password = password)
        user_info =  UserInfo.objects.create(user  =  user  ,  name  =  name  ,  email =  email ,  image  =  image)
        user.save()
        user_info.save()
        login(request  , user)
        messages.success(request ,  "Registration successful")
        return  redirect('index')

    return render(request ,  'chat/register.html')


def loginView(request) :
    if request.method  ==  'POST' :
        username =  request.POST['username']
        password =  request.POST['password']

        user  = authenticate(request, username=username, password=password)

        if user:
            login(request  , user)
            return redirect('index')
        else  :
            messages.error(request , "Invalid username or Password")

    return render(request , 'chat/login.html')



@login_required
def index(request):
    user = request.user
    chatrooms = ChatRoom.objects.filter(participants=user).distinct()

    # Add other participant info to each room object
    for room in chatrooms:
        other = room.participants.exclude(id=user.id).first()
        room.other_user = other  # dynamically attach for template use

    return render(request, 'chat/index.html', {'chatrooms': chatrooms})


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def search(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(userinfo__name__icontains=query) |
            Q(userinfo__email__icontains=query)
        ).exclude(id=request.user.id).distinct()

    return render(request, 'chat/search.html', {'query': query, 'users': users})



@login_required
def chatroom(request ,  id) :
    room  =  get_object_or_404(ChatRoom , id =  id)

    if request.user not in room.participants.all() :
        return redirect('index')
    messages =  room.messages.all()
    print(messages)
    return render(request ,  'chat/chatroom.html' ,  {
        'room' : room , 'messages' : messages
    })


from django.shortcuts import get_object_or_404

@login_required
def add_user_to_chatroom(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    sender = request.user

    chatroom_qs = ChatRoom.objects.filter(participants=sender).filter(participants=receiver)

    if chatroom_qs.exists():
        chatroom = chatroom_qs.first()
    else:
        name = f"{receiver.username}-{sender.username}"
        chatroom = ChatRoom.objects.create(name=name)
        chatroom.participants.add(receiver, sender)
        chatroom.save()

    return redirect('chatroom', id=chatroom.id)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login page URL name