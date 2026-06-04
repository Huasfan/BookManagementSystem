from django.shortcuts import render
from bookmanagement.models import Borrows

def index(request):
    borrows = Borrows.objects.values("username__username", "book__bookname", "borrowdate", "returntype")
    return render(request, 'index.html', {'borrows': borrows})

