from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


@login_required(login_url='login')
def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = TopicModel.objects.all()
    room = RoomModel.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = room.count()
    room_message = MessageModel.objects.filter(Q(room__topic__name__icontains=q))
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
        'topics': topic,
        'rooms': room,
        'room_count': room_count,
        'room_message': room_message,
    }
    return render(request, 'main/index.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You're Successful Registered")
            return redirect('login')
        else:
            messages.info(request, 'Sign Up before Log in')
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    room = user.roommodel_set.all()
    topic = TopicModel.objects.all()
    room_message = user.messagemodel_set.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile', pk=user.id)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profilemodel)
    context = {'user': user, 'topics': topic, 'room_message': room_message,
               'rooms': room, 'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/user_profile.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
    context = {}
    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def create_room(request):
    form = CreateRoomForm()
    if request.method == 'POST':
        form = CreateRoomForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.host = request.user
            instance.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    model = RoomModel.objects.get(id=pk)
    if request.method == 'POST':
        form = CreateRoomForm(request.POST or None, instance=model)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CreateRoomForm(instance=model)
    context = {
        'form': form
    }
    return render(request, 'main/edit.html', context)


@login_required(login_url='login')
def room_details(request, pk):
    form = CommentModelForm()
    model = RoomModel.objects.get(id=pk)
    message_id = MessageModel.objects.get(id=pk)
    room_message = model.messagemodel_set.all()
    participants = model.participants.all()
    count_participants = participants.count()
    if request.method == 'POST':
        form = CommentModelForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.room = model
            instance.save()
            return redirect('room_details', pk=model.id)
    if request.method == 'POST':
        p_form = CommentUpdateForm(request.POST or None, instance=message_id)
        if p_form.is_valid():
            instance_p = p_form.save(commit=False)
            instance_p.user = request.user
            instance_p.save()
            return redirect('room_details', pk=model.id)
    else:
        p_form = CommentUpdateForm(instance=message_id)
    context = {'model': model, 'room_message': room_message, 'form': form,
               'p_form': p_form,
               'participants': participants,
               'count_participants': count_participants}
    return render(request, 'main/details.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    model = RoomModel.objects.get(id=pk)
    if request.method == 'POST':
        model.delete()
        return redirect('/')
    context = {}
    return render(request, 'main/delete.html', context)
