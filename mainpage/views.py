from django.shortcuts import render

def main_page(request):
    return render(request,'mainpage/main.html')

def about_page(request):
    return render(request,'mainpage/about.html')

def login_page(request):
    return render(request,'mainpage/login.html')
