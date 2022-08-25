from multiprocessing import context
from django.shortcuts import render
from .models import Room



# Create your views here.


def home(request):
    rooms= Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'appbase/home.html', context)


def room(request, pk):
    room = Room.objects.get(id = pk)
    context = {'room': room}
    return render(request, 'appbase/room.html',context)

def createRoom(request):
    context={}
    return render(request, 'appbase/room_form.html',context)