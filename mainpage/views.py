from django.shortcuts import render

def main_page(request):
    return render(request,'mainpage.html')

def about_page(request):
    return render(request,'about.html')
