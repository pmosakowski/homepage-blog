from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from mainpage.forms import LoginForm

def main_page(request):
    return render(request,'mainpage/main.html')

def about_page(request):
    return render(request,'mainpage/about.html')

def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            credentials = {
                    'username': login_form.cleaned_data['username'],
                    'password': login_form.cleaned_data['password']
            }
            user = authenticate(**credentials)
            if user is not None:
                login(request,user)
                return redirect('/blog')
    else:
    
        login_form = LoginForm()
    
    return render(request,'mainpage/login.html',{'form': login_form})

def logout_page(request):
    logout(request)
    return redirect('/')
