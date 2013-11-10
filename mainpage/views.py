from django.shortcuts import render
from mainpage.forms import LoginForm

def main_page(request):
    return render(request,'mainpage/main.html')

def about_page(request):
    return render(request,'mainpage/about.html')

def login_page(request):
    login_form = LoginForm()

    return render(request,'mainpage/login.html',{'form': login_form})
