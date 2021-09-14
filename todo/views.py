from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError


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


def dashboard(request):
    return render(request, 'todo/dashboard.html')

