from django.shortcuts import render
from django import template
from django.http import HttpResponse

def home(request):

	return render(request, 'templates/static_handler.html')

# Create your views here.
