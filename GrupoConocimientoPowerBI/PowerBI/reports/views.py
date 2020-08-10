from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect, render



# Create your views here.
def index(request):
    return render(request,'reports/index.html')
    