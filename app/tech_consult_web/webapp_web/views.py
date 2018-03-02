from django.shortcuts import render
from django.shortcuts import render_to_response

import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, "index.html", context_dict)

def request_detail(request, consumerRequest_pk):
    context_dict = {}
    return render(request, "request_detail.html", context_dict)