from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request): #List of Consult
    return render(request,"list.html",{
        'form' : UserCreationForm,
        'title': "Tratando de armar un formulario"
    })
    
def put_consult(request):# post form
    return ""

def get_consult(request): # get consult
    return ""

def del_consult(request):# post form
    return ""

#------  Dr  -----------------------------

def list_dr(request):
    return ""

def put_dr():    
    return ""

def get_dr():
    return ""

def del_dr():
    return ""

# ------ Person -------------------
def list_person():
    return ""

def put_person():
    return ""

def get_person():
    return ""

def del_person():
    return ""