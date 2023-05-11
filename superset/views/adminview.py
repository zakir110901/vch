from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ..models import Uvstudents

@login_required
def admindashboard(request):
    return render(request,'superset/admindashboard.html',{"count":0})

@login_required
def Ustudents(request):
    x=Uvstudents.objects.all()
    return render(request,'superset/admindashboard.html',{"count":1,"x":x})