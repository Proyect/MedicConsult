from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request,"list.html",{
        'form' : UserCreationForm
    })
