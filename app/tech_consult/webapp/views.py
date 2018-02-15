from django.shortcuts import render
from django.shortcuts import render_to_response

import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Consumer, ConsumerRequest, Producer, Review
from .forms import UpdateConsumerForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):

    return HttpResponse("CS4501 Project 2")

# json response code based on https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python
def get_consumer (request, consumer_pk):
    response = {}
    response_data = {}

    if request.method == 'GET':
        try:
            consumer = Consumer.objects.get(pk=consumer_pk)

            response['ok'] = True

            #Uncommented until we load database with data
            response_data['pk'] = consumer.pk
            response_data['username'] = consumer.username
            response_data['password'] = consumer.password
            response_data['first_name'] = consumer.first_name
            response_data['last_name'] = consumer.last_name
            response_data['phone'] = consumer.phone
            response_data['email'] = consumer.email


            #response_data['pk'] = 1
            #response_data['username'] = 'myl2vu'
            #response_data['password'] = 'ilikeseals'
            #response_data['first_name'] = 'marissa'
            #response_data['last_name'] = 'lee'
            #response_data['phone'] = '7037316926'
            #response_data['email'] = 'myl2vu@virginia.edu'

        except Consumer.DoesNotExist:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_consumer (request):
    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = UpdateConsumerForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Creating the consumer based on form input
                consumer = Consumer()
                consumer.username = form.cleaned_data['username']
                consumer.password = form.cleaned_data['password']
                consumer.first_name = form.cleaned_data['first_name']
                consumer.last_name = form.cleaned_data['last_name']
                consumer.phone = form.cleaned_data['phone']
                consumer.email = form.cleaned_data['email']

                consumer.save()

                # Adding the created consumer's data to json response
                response_data['pk'] = consumer.pk
                response_data['username'] = consumer.username
                response_data['password'] = consumer.password
                response_data['first_name'] = consumer.first_name
                response_data['last_name'] = consumer.last_name
                response_data['phone'] = consumer.phone
                response_data['email'] = consumer.email

            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)


        else:
            # An unfilled form gets displayed
            form = UpdateConsumerForm()
            return render(request, 'update_consumer.html', {'form': form, 'update': False})
    except:
        response['ok'] = False

        response['result'] = response_data


    return JsonResponse(response)


@csrf_exempt
def update_consumer (request, consumer_pk):
    response = {}
    response_data = {}
    try:
        consumer = Consumer.objects.get(pk=consumer_pk)

        # User submits the form's data
        if request.method == 'POST':
            form = UpdateConsumerForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Updating the consumer based on form input
                consumer.username = form.cleaned_data['username']
                consumer.password = form.cleaned_data['password']
                consumer.first_name = form.cleaned_data['first_name']
                consumer.last_name = form.cleaned_data['last_name']
                consumer.phone = form.cleaned_data['phone']
                consumer.email = form.cleaned_data['email']

                consumer.save()

                # Adding the updated consumer's data to json response
                response_data['pk'] = consumer.pk
                response_data['username'] = consumer.username
                response_data['password'] = consumer.password
                response_data['first_name'] = consumer.first_name
                response_data['last_name'] = consumer.last_name
                response_data['phone'] = consumer.phone
                response_data['email'] = consumer.email

            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)

        # The form filled with the consumer's data
        #else:
        #    form = UpdateConsumerForm(initial={'username':consumer.username, 'password': consumer.password, 'first_name': consumer.first_name, 'last_name': consumer.last_name, 'phone': consumer.phone, 'email': consumer.email})
        #    return render(request, 'update_consumer.html', {'form': form, 'update': True})

    except:
        response['ok'] = False

        response['result'] = response_data


    return JsonResponse(response)

#Does not yet work with Postman
@csrf_exempt
def delete_consumer (request, consumer_pk):
    if request.method == 'POST':
        response = {}
        response_data = {}

        try:
            consumer = Consumer.objects.get(pk=consumer_pk)

            response['ok'] = True

            # Adding the deleted consumer's data to json response
            response_data['pk'] = consumer.pk
            response_data['username'] = consumer.username
            response_data['password'] = consumer.password
            response_data['first_name'] = consumer.first_name
            response_data['last_name'] = consumer.last_name
            response_data['phone'] = consumer.phone
            response_data['email'] = consumer.email

            consumer.delete()

        except Consumer.DoesNotExist:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)


def get_producer (request, producer_pk):
    response = {}
    response_data = {}

    if request.method == 'GET':
        try:
            producer = Producer.objects.get(pk=producer_pk)

            response['ok'] = True

            #Uncommented until we load database with data
            response_data['pk'] = producer.pk
            response_data['username'] = producer.username
            response_data['password'] = producer.password
            response_data['first_name'] = producer.first_name
            response_data['last_name'] = producer.last_name
            response_data['phone'] = producer.phone
            response_data['email'] = producer.email
            response_data['bio'] = producer.bio
            response_data['skills'] = producer.skills

            #response_data['pk'] = 1
            #response_data['username'] = 'myl2vu'
            #response_data['password'] = 'ilikeseals'
            #response_data['first_name'] = 'marissa'
            #response_data['last_name'] = 'lee'
            #response_data['phone'] = '7037316926'
            #response_data['email'] = 'myl2vu@virginia.edu'

        except Producer.DoesNotExist:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

def create_producer (request):
    response = {}
    response_data = {}

    if request.method == 'POST':
        form = UpdateProducerForm(request.POST)

        if form.is_valid():

            response['ok'] = True

            # Creating the producer based on form input
            producer = Producer()
            producer.username = form.cleaned_data['username']
            producer.password = form.cleaned_data['password']
            producer.first_name = form.cleaned_data['first_name']
            producer.last_name = form.cleaned_data['last_name']
            producer.phone = form.cleaned_data['phone']
            producer.email = form.cleaned_data['email']
            producer.bio = form.cleaned_data['bio']
            producer.skills = form.cleaned_data['skills']

            producer.save()

            # Adding the created producer's data to json response
            response_data['pk'] = producer.pk
            response_data['username'] = producer.username
            response_data['password'] = producer.password
            response_data['first_name'] = producer.first_name
            response_data['last_name'] = producer.last_name
            response_data['phone'] = producer.phone
            response_data['email'] = producer.email
            response_data['bio'] = producer.bio
            response_data['skills'] = producer.skills

        else:
            response['ok'] = False

        response['result'] = response_data

        return JsonResponse(response)

    else:
        # An unfilled form gets displayed
        form = UpdateProducerForm()
        return render(request, 'update_producer.html', {'form': form, 'update': False})

def update_producer (request, producer_pk):
    response = {}
    response_data = {}
    try:
        producer = Producer.objects.get(pk=producer_pk)

        # User submits the form's data
        if request.method == 'POST':
            form = UpdateProducerForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Updating the producer based on form input
                producer.username = form.cleaned_data['username']
                producer.password = form.cleaned_data['password']
                producer.first_name = form.cleaned_data['first_name']
                producer.last_name = form.cleaned_data['last_name']
                producer.phone = form.cleaned_data['phone']
                producer.email = form.cleaned_data['email']
                producer.bio = form.cleaned_data['bio']
                producer.skills = form.cleaned_data['skills']

                producer.save()

                # Adding the updated producer's data to json response
                response_data['pk'] = producer.pk
                response_data['username'] = producer.username
                response_data['password'] = producer.password
                response_data['first_name'] = producer.first_name
                response_data['last_name'] = producer.last_name
                response_data['phone'] = producer.phone
                response_data['email'] = producer.email
                response_data['bio'] = producer.bio
                response_data['skills'] = producer.skills

            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)

        # The form filled with the producer's data
        else:
            form = UpdateProducerForm(initial={'username':producer.username, 'password': producer.password, 'first_name': producer.first_name, 'last_name': producer.last_name, 'phone': producer.phone, 'email': producer.email})
            return render(request, 'update_producer.html', {'form': form, 'update': True})

    except Producer.DoesNotExist:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

def delete_producer (request, producer_pk):
    response = {}
    response_data = {}

    try:
        producer = Producer.objects.get(pk=producer_pk)

        response['ok'] = True

        # Adding the deleted producer's data to json response
        response_data['pk'] = producer.pk
        response_data['username'] = producer.username
        response_data['password'] = producer.password
        response_data['first_name'] = producer.first_name
        response_data['last_name'] = producer.last_name
        response_data['phone'] = producer.phone
        response_data['email'] = producer.email
        response_data['bio'] = producer.bio
        response_data['skills'] = producer.skills 

        producer.delete()

    except Producer.DoesNotExist:
        response['ok'] = False

    response['result'] = response_data

    return JsonResponse(response)
