from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from bookmanagement.models import Borrows


def index(request):
    borrows = Borrows.objects.values("username__username", "book__bookname", "borrowdate", "returntype")
    return render(request, 'index.html', {'borrows': borrows})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

