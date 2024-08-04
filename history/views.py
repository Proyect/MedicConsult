from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request): #List of Date
    return render(request,"list.html",{
        'form' : UserCreationForm,
        'title': "Tratando de armar un formulario"
    })
    
def update(request):
    return ""
