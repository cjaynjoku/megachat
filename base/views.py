from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
# Create your views here.

# rooms = [
#     {'id':1, 'name':'lets learn Python!'},
#     {'id':2, 'name':'Design with me!'},
#     {'id':3, 'name':'Front end guys get in here'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = user.objects.get(username=username)
        except:
            pass
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) #creates a session in the db and browser
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    context = {'page':page}
    
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', context)

def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.rooms.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q)| 
        Q(description__icontains = q)) #.order_by('-created')
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)
    
def room(request, pk):
    room = Room.rooms.get(id = pk)
    room_messages = room.message_set.all().order_by("-created")
    
    if request.method =="POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.rooms.get(id = pk)
    form = RoomForm(instance = room)
    
    
    if request.user != room.host:    
        return HttpResponse("Your are not the room creator")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.rooms.get(id = pk)
    context ={'obj':room}
    
    if request.user != room.host:
        return HttpResponse("You are not the room creator")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request, "base/delete.html", context)
    
    
    # room.delete()
    # if()
    # return redirect('home')
