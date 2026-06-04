from django.shortcuts import render
from bookmanagement.models import Borrows

def index(request):
    borrows = Borrows.objects.filter(returntype=0).values("username__username", "book__bookname", "borrowdate")
    return render(request, 'index.html', {'borrows': borrows})

