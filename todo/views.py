from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from todo.forms import TodoForm


def homepage(request):
    return render(request, 'todo/homepage.html')


def signup_user(request):
    context = {
        'form': UserCreationForm()
    }
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', context)
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                context['error'] = 'This user name is already taken, please use another one'
                return render(request, 'todo/signup_user.html', context)
        else:
            context['error'] = 'Password not match, please try again'
            return render(request, 'todo/signup_user.html', context)


def login_user(request):
    context = {
        'form': AuthenticationForm()
    }
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', context)
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context['error'] = 'Login failed, please check your username and password'
            return render(request, 'todo/login_user.html', context)
        else:
            login(request, user)
            return redirect('dashboard')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')


def dashboard(request):
    return render(request, 'todo/dashboard.html')


def create_todo(request):
    context = {
        'form': TodoForm()
    }
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', context)

    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('dashboard')

        except ValueError:
            context['error'] = 'Some field have not correct format, please check.'
            return render(request, 'todo/create_todo.html', context)
