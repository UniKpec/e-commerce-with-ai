from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import create_user,login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout

def signUpView(request):
    if request.method == "POST":
        form = create_user(request.POST)   
        if form.is_valid(): #eğer valid değilse template kısmında bunu göstereceğiz.
            user = form.save()
            login(request,user)
            return redirect("shop:home")
    else:
        form = create_user()    
    return render(request,"shop/signup.html",context={"forms":form})

def logInView(request):
    if request.method == "POST":
        form = login_user(request,data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("shop:home")
    else:
        form = login_user()
    return render(request,"shop/login.html",context={"forms":form})

def logout_view(request):
    logout(request)
    return redirect('shop:login')

def index(request):
    return render(request,"base.html")

# Create your views here.


