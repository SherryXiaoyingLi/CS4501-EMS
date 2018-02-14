from django.shortcuts import render
from django.shortcuts import render_to_response

import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Consumer, ConsumerRequest, Producer, Review

# Create your views here.

def index(request):
    return HttpResponse("CS4501 Project 2")

def get_consumer (request, consumer_pk):
    #consumer = Consumer.objects.get(pk=consumer_pk)
    response_data = {}
    if request.method == 'GET':

        #Uncommented until we load database with data
        #response_data['pk'] = consumer.pk
        #response_data['username'] = consumer.username
        #response_data['password'] = consumer.password
        #response_data['first_name'] = consumer.first_name
        #response_data['last_name'] = consumer.last_name
        #response_data['phone'] = consumer.phone
        #response_data['email'] = consumer.email

        response_data['pk'] = 1
        response_data['username'] = 'myl2vu'
        response_data['password'] = 'ilikeseals'
        response_data['first_name'] = 'marissa'
        response_data['last_name'] = 'lee'
        response_data['phone'] = '7037316926'
        response_data['email'] = 'myl2vu@virginia.edu'

        #return JsonResponse({'test': 'value'})
        return JsonResponse(response_data)
    elif request.method == 'POST':

        # consumer.save()

        # Uncommented until we load database with data
        # response_data['pk'] = consumer.pk
        # response_data['username'] = consumer.username
        # response_data['password'] = consumer.password
        # response_data['first_name'] = consumer.first_name
        # response_data['last_name'] = consumer.last_name
        # response_data['phone'] = consumer.phone
        # response_data['email'] = consumer.email

        return JsonResponse(response_data)
    return HttpResponse("Needs a GET or POST operation")