from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

from todo.forms import TodoForm
from todo.models import Todo


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


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')


@login_required
def dashboard(request):
    todos = Todo.objects.filter(user=request.user, completed_time__isnull=True)\
                        .all()
    context = {
        'todos': todos
    }
    return render(request, 'todo/dashboard.html', context)


@login_required
def completed_todo(request):
    todos = Todo.objects.filter(user=request.user, completed_time__isnull=False)\
                        .order_by('-completed_time')\
                        .all()
    context = {
        'todos': todos
    }
    return render(request, 'todo/completed_todo.html', context)


@login_required
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


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'todo': todo,
            'form': form
        }
        return render(request, 'todo/view_todo.html', context)
    elif request.method == 'POST':
        form = TodoForm(data=request.POST, instance=todo)
        form.save()
        return redirect('dashboard')


@login_required
def complete_todo(request, todo_pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        todo.completed_time = timezone.now()
        todo.save()
        return redirect('dashboard')


@login_required
def delete_todo(request, todo_pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
        todo.delete()
        return redirect('dashboard')
