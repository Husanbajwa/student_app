from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from .models import *
from .forms import *


def index(request):
    return render(request, 'appbase/index.html')

def loginPage(request):
    page='login'
    # remove login again manual(user can't login again if he is already loggedin)  
    if request.user.is_authenticated :
        return redirect('home')
    if request.method =='POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user =User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, email=email , password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist ')
    context={'page':page}
    return render(request, 'appbase/login_registration.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=MyUserCreationForm()
# save user data in database
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An ERROR occured during registration')

    context={'form':form}
    return render(request, 'appbase/login_registration.html',context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms= Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    topics =Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'appbase/home.html', context)


def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages =room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {
            'room': room,
            'room_messages':room_messages,
            'participants':participants
            }
    return render(request, 'appbase/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        try:
            thread = Thread.objects.create(
            first_person = user,
            second_person = request.user,
            )
            return redirect('messages')
        except IntegrityError:
            # thread already exists, it shows the messages page itself
            return redirect('messages')

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms': rooms,'room_messages':room_messages,'topics':topics}
    return render(request , 'appbase/profile.html',context)




@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics =Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        image = request.FILES.get('image', '')
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image = image
        )
        return redirect('home')
    context={'form':form, 'topics':topics}
    return render(request, 'appbase/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form=RoomForm(instance=room)
    topics =Topic.objects.all()
    
    if (request.user != room.host):
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.image = request.FILES.get('image', '')

        room.save()
        return redirect('home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request, 'appbase/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'appbase/delete.html' ,{'obj':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')


    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'appbase/delete.html' ,{'obj':message})

    
@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form =UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk = user.id)
    context={'form':form}
    return render(request,'appbase/update-user.html',context)


def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request,'appbase/topic.html',context)


def activityPage(request):
    room_messages = Message.objects.all()
    context={"room_messages":room_messages}
    return render(request,'appbase/activity.html',context)

@login_required
def messages_page(request):
    # threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        'Threads': threads
    }
    return render(request,'appbase/message.html',context)




# # blog views
# def blog_detail(request, slug):
#     context = {}
#     try:
#         blog_obj = BlogModel.objects.filter(slug=slug).first()
#         context['blog_obj'] = blog_obj
#     except Exception as e:
#         print(e)
#     return render(request, 'appbase/blog/blog_detail.html', context)


# def see_blog(request):
#     context = {}

#     try:
#         blog_objs = BlogModel.objects.filter(user=request.user)
#         context['blog_objs'] = blog_objs
#     except Exception as e:
#         print(e)

#     print(context)
#     return render(request, 'appbase/blog/see_blog.html', context)


# def add_blog(request):
#     context = {'form': BlogForm}
#     try:
#         if request.method == 'POST':
#             form = BlogForm(request.POST)
#             print(request.FILES)
#             image = request.FILES.get('image', '')
#             title = request.POST.get('title')
#             user = request.user

#             if form.is_valid():
#                 print('Valid')
#                 content = form.cleaned_data['content']

#             blog_obj = BlogModel.objects.create(
#                 user=user, title=title,
#                 content=content, image=image
#             )
#             print(blog_obj)
#             return redirect('/add-blog/')
#     except Exception as e:
#         print(e)

#     return render(request, 'appbase/blog/add_blog.html', context)


# # def blog_update(request, slug):
# #     context = {}
# #     try:

# #         blog_obj = BlogModel.objects.get(slug=slug)

# #         if blog_obj.user != request.user:
# #             return redirect('/')

# #         initial_dict = {'content': blog_obj.content}
# #         form = BlogForm(initial=initial_dict)
# #         if request.method == 'POST':
# #             form = BlogForm(request.POST)
# #             print(request.FILES)
# #             image = request.FILES['image']
# #             title = request.POST.get('title')
# #             user = request.user

# #             if form.is_valid():
# #                 content = form.cleaned_data['content']

# #             blog_obj = BlogModel.objects.create(
# #                 user=user, title=title,
# #                 content=content, image=image
# #             )

# #         context['blog_obj'] = blog_obj
# #         context['form'] = form
# #     except Exception as e:
# #         print(e)

# #     return render(request, 'appbase/blog/update_blog.html', context)

# def blog_update(request, slug):
#     context = {}
#     try:
#         blog_obj = BlogModel.objects.get(slug=slug)

#         if blog_obj.user != request.user:
#             return redirect('/')

#         initial_dict = {'content': blog_obj.content}
#         form = BlogForm(initial=initial_dict)

#         if request.method == 'POST':
#             form = BlogForm(request.POST, request.FILES)
#             if form.is_valid():
#                 content = form.cleaned_data['content']
#                 title = form.cleaned_data['title']
#                 # image = form.cleaned_data.get('image')
#                 # if image:
#                 #     blog_obj.image = image
#                 blog_obj.content = content
#                 blog_obj.title = title
#                 blog_obj.save()
#                 return redirect('see_blog')

#         context['blog_obj'] = blog_obj
#         context['form'] = form

#     except BlogModel.DoesNotExist:
#         print(f"Blog with slug {slug} does not exist")
#     except Exception as e:
#         print(e)

#     return render(request, 'appbase/blog/update_blog.html', context)


# def blog_delete(request, id):
#     try:
#         blog_obj = BlogModel.objects.get(id=id)

#         if blog_obj.user == request.user:
#             blog_obj.delete()

#     except Exception as e:
#         print(e)

#     return redirect('/see-blog/')

