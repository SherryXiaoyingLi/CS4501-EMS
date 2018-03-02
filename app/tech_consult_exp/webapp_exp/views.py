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

# For index page
# Returns the pk of the newest consumer request
def getNewestRequestPk(request):
    response = {}
    return JsonResponse(response)

# For index page
# Returns the pk of the consumer request with the highest price
def getHighestRequestPk(request):
    response = {}
    return JsonResponse(response)

# For request detail page
# Returns the request information, consumer information, and producer username
def getRequestDetail(request, consumerRequest_pk):
    response = {}
    return JsonResponse(response)
