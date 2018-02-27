from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.http import JsonResponse

import urllib.request
import urllib.parse
import json

# Create your views here.
def index(request):

    return HttpResponse("CS4501 Project 3, Experience layer")