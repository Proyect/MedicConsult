from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request): #List of Consult
    return render(request,"list.html",{
        'form' : UserCreationForm,
        'title': "Tratando de armar un formulario"
    })
    
def update_consult(request):
    return ""

def insert_consult(request):
    return ""

def get_consult(request):
    return ""

#------  Dr  -----------------------------

def list_dr(request):
    return ""