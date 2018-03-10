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
    context_dict = {‘newest_pk’: 1, ‘highest_pk’: 1}
    return render(request, "index.html", context_dict)

def request_detail(request, consumerRequest_pk):
    context_dict = {‘title’: ‘New to AWS, ‘description’: ‘Looking for someone to teach me AWS’, ‘offered_price’: 75.0, ‘timestamp’: ‘March 9, 2018.  7:55’, ‘availability’: ‘Mondays and Wednesdays’, ‘consumer_username’: ‘bob1’, ‘consumer_email’: ‘bob1@gmail.com’, ‘consumer_phone’: ‘434-958-2913’, ‘producer_username’: null}
    return render(request, "request_detail.html", context_dict)
