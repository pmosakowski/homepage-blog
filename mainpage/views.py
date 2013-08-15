from django.shortcuts import render

def main_page(request):
    return render(request,'base.html')

def about_page(request):
    return render(request,'about.html')
