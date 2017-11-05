from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request, template_name='routes/index.html'):
	data = {}
	return render(request, template_name, data)
