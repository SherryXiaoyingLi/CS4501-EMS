from django.shortcuts import render
from django.shortcuts import render_to_response

import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Consumer, ConsumerRequest, Producer, Review, Authenticator
from .forms import CreateConsumerForm, CreateProducerForm, CreateReviewForm, CreateConsumerRequestForm, CreateAuthenticatorForm, EnterAuthenticatorForm, LoginForm
from .forms import UpdateConsumerForm, UpdateReviewForm, UpdateConsumerRequestForm, UpdateProducerForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.conf import settings
import datetime
import os
import hmac
import urllib.request
import urllib.parse

# Create your views here.

def index(request):
    return HttpResponse("CS4501 Project 3, Microservice layer")

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

        except:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_consumer (request):
    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = CreateConsumerForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Creating the consumer based on form input
                consumer = Consumer()
                consumer.username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                consumer.password = make_password(password, salt=None, hasher='default')
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
            form = CreateConsumerForm()
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

                # Updating the consumer based on form input, only for filled fields
                if form.cleaned_data['username']:
                    consumer.username = form.cleaned_data['username']
                if form.cleaned_data['password']:
                    password = form.cleaned_data['password']
                    consumer.password = make_password(password, salt=None, hasher='default')
                if form.cleaned_data['first_name']:
                    consumer.first_name = form.cleaned_data['first_name']
                if form.cleaned_data['last_name']:
                    consumer.last_name = form.cleaned_data['last_name']
                if form.cleaned_data['phone']:
                    consumer.phone = form.cleaned_data['phone']
                if form.cleaned_data['email']:
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
        else:
            form = UpdateConsumerForm(initial={'username':consumer.username, 'first_name': consumer.first_name, 'last_name': consumer.last_name, 'phone': consumer.phone, 'email': consumer.email})
            return render(request, 'update_consumer.html', {'form': form, 'update': True})

    except:
        response['ok'] = False

        response['result'] = response_data


    return JsonResponse(response)

#Does not yet work with Postman
@csrf_exempt
def delete_consumer (request, consumer_pk):

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
    except:
        response['ok'] = False
    response['result'] = response_data
    return JsonResponse(response)

#@csrf_exempt
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

        except:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_producer (request):
    response = {}
    response_data = {}
    try:
      if request.method == 'POST':
        form = CreateProducerForm(request.POST)

        if form.is_valid():

            response['ok'] = True

            # Creating the producer based on form input
            producer = Producer()
            producer.username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            producer.password = make_password(password, salt=None, hasher='default')
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
        form = CreateProducerForm()
        return render(request, 'update_producer.html', {'form': form, 'update': False})
    except:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
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

                # Updating the producer based on form input, only for filled fields
                if form.cleaned_data['username']:
                    producer.username = form.cleaned_data['username']
                if form.cleaned_data['password']:
                    password = form.cleaned_data['password']
                    producer.password = make_password(password, salt=None, hasher='default')
                if form.cleaned_data['first_name']:
                    producer.first_name = form.cleaned_data['first_name']
                if form.cleaned_data['last_name']:
                    producer.last_name = form.cleaned_data['last_name']
                if form.cleaned_data['phone']:
                    producer.phone = form.cleaned_data['phone']
                if form.cleaned_data['email']:
                    producer.email = form.cleaned_data['email']
                if form.cleaned_data['bio']:
                    producer.bio = form.cleaned_data['bio']
                if form.cleaned_data['skills']:
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
            form = UpdateProducerForm(initial={'username':producer.username, 'first_name': producer.first_name, 'last_name': producer.last_name, 'phone': producer.phone, 'email': producer.email, 'bio': producer.bio, 'skills': producer.skills})
            return render(request, 'update_producer.html', {'form': form, 'update': True})

    except:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
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
    except:
        response['ok'] = False

    response['result'] = response_data
    return JsonResponse(response)


def get_review(request, review_pk):
    response = {}
    response_data = {}

    if request.method == 'GET':
        try:
            review = Review.objects.get(pk=review_pk)

            response['ok'] = True

            # Uncommented until we load database with data
            response_data['pk'] = review.pk
            response_data['rating'] = review.rating
            response_data['author'] = review.author.pk
            response_data['comment'] = review.comment
            response_data['producer'] = review.producer.pk

        except:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_review(request):
    response = {}
    response_data = {}

    try:
        if request.method == 'POST':
            form = CreateReviewForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Creating the consumer based on form input
                review = Review()
                review.rating = int(form.cleaned_data['rating'])
                author = Consumer.objects.get(pk = int(form.cleaned_data['author']))
                review.author = author
                review.comment = form.cleaned_data['comment']
                producer = Producer.objects.get(pk = int(form.cleaned_data['producer']))
                review.producer = producer

                review.save()

                # Adding the created consumer's data to json response
                response_data['pk'] = review.pk
                response_data['rating'] = review.rating
                response_data['author'] = review.author.pk
                response_data['comment'] = review.comment
                response_data['producer'] = review.producer.pk

            else:
                response['ok'] = False

        else:
            # An unfilled form gets displayed
            form = CreateReviewForm()
            return render(request, 'update_review.html', {'form': form, 'update': False})

    except:
        response['ok'] = False
    response['result'] = response_data



    return JsonResponse(response)

@csrf_exempt
def update_review(request, review_pk):
    response = {}
    response_data = {}
    try:
        review = Review.objects.get(pk=review_pk)

        # User submits the form's data
        if request.method == 'POST':
            form = UpdateReviewForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Updating the review based on form input only if the fields are filled in
                if form.cleaned_data['rating']:
                    review.rating = int(form.cleaned_data['rating'])
                if form.cleaned_data['author']:
                    author = Consumer.objects.get(pk = int(form.cleaned_data['author']))
                    review.author = author
                if form.cleaned_data['comment']:
                    review.comment = form.cleaned_data['comment']
                if form.cleaned_data['producer']:
                    producer = Producer.objects.get(pk = int(form.cleaned_data['producer']))
                    review.producer = producer

                review.save()

                # Adding the updated consumer's data to json response
                response_data['pk'] = review.pk
                response_data['rating'] = review.rating
                response_data['author'] = review.author.pk
                response_data['comment'] = review.comment
                response_data['producer'] = review.producer.pk


            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)

        # The form filled with the consumer's data
        else:
            form = UpdateReviewForm(
                                    initial={'rating': review.rating, 'author': review.author.pk, 'comment': review.comment,'producer':review.producer.pk})
            return render(request, 'update_review.html', {'form': form, 'update': True})

    except Review:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def delete_review(request, review_pk):
    response = {}
    response_data = {}

    try:
        review = Review.objects.get(pk=review_pk)

        response['ok'] = True

        # Adding the deleted consumer's data to json response
        response_data['pk'] = review.pk
        response_data['rating'] = review.rating
        response_data['author'] = review.author.pk
        response_data['comment'] = review.comment
        response_data['producer'] = review.producer.pk

        review.delete()

    except:
        response['ok'] = False

    response['result'] = response_data

    return JsonResponse(response)


def get_consumerRequest(request, consumerRequest_pk):
    response = {}
    response_data = {}

    if request.method == 'GET':
        try:
            consumerRequest = ConsumerRequest.objects.get(pk=consumerRequest_pk)

            response['ok'] = True

            # Uncommented until we load database with data
            response_data['pk'] = consumerRequest.pk
            response_data['title'] = consumerRequest.title
            response_data['offered_price'] = consumerRequest.offered_price
            response_data['description'] = consumerRequest.description
            response_data['availability'] = consumerRequest.availability
            response_data['consumer'] = consumerRequest.consumer.pk
            if consumerRequest.accepted_producer != None:
                response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
            else:
                response_data['accepted_producer'] = None


        except:
            response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_consumerRequest(request):

    response = {}
    response_data = {}
    try:
      if request.method == 'POST':
        form = CreateConsumerRequestForm(request.POST)

        if form.is_valid():

            response['ok'] = True

            # Creating the consumer based on form input
            consumerRequest = ConsumerRequest()
            consumerRequest.timestamp = datetime.date.today().strftime("%B %d, %Y")
            consumerRequest.title = form.cleaned_data['title']
            consumerRequest.offered_price = float(form.cleaned_data['offered_price'])
            consumerRequest.description = form.cleaned_data['description']
            consumerRequest.availability = form.cleaned_data['availability']
            consumer = Consumer.objects.get(pk = int(form.cleaned_data['consumer']))
            consumerRequest.consumer = consumer
            #producer = Producer.objects.get(pk = int(form.cleaned_data['accepted_producer']))
            if form.cleaned_data['accepted_producer']:
                producer = Producer.objects.get(pk = int(form.cleaned_data['accepted_producer']))
                consumerRequest.accepted_producer = producer

            consumerRequest.save()

            # Adding the created consumer's data to json response
            response_data['pk'] = consumerRequest.pk
            response_data['title'] = consumerRequest.title
            response_data['offered_price'] = consumerRequest.offered_price
            response_data['description'] = consumerRequest.description
            response_data['timestamp'] = consumerRequest.timestamp
            response_data['availability'] = consumerRequest.availability
            response_data['consumer'] = consumerRequest.consumer.pk
            if consumerRequest.accepted_producer != None:
                response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
            else:
                response_data['accepted_producer'] = None
        else:
            response['ok'] = False

        response['result'] = response_data

        return JsonResponse(response)

      else:
        # An unfilled form gets displayed
        form = CreateConsumerRequestForm()
        return render(request, 'update_consumerRequest.html', {'form': form, 'update': False})
    except:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def update_consumerRequest(request, consumerRequest_pk):
    response = {}
    response_data = {}
    try:
        consumerRequest = ConsumerRequest.objects.get(pk=consumerRequest_pk)

        # User submits the form's data
        if request.method == 'POST':
            form = UpdateConsumerRequestForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Updating the consumer request based on form input if the forms are filled
                if form.cleaned_data['title']:
                    consumerRequest.title = form.cleaned_data['title']
                if form.cleaned_data['offered_price']:
                    consumerRequest.offered_price = float(form.cleaned_data['offered_price'])
                if form.cleaned_data['description']:
                    consumerRequest.description = form.cleaned_data['description']
                if form.cleaned_data['availability']:
                    consumerRequest.availability = form.cleaned_data['availability']
                if form.cleaned_data['consumer']:
                    consumer = Consumer.objects.get(pk = int(form.cleaned_data['consumer']))
                    consumerRequest.consumer = consumer
                if form.cleaned_data['accepted_producer']:
                    producer = Producer.objects.get(pk = int(form.cleaned_data['accepted_producer']))
                    consumerRequest.accepted_producer = producer

                consumerRequest.save()

                # Adding the updated consumer request's data to json response
                response_data['pk'] = consumerRequest.pk
                response_data['title'] = consumerRequest.title
                response_data['offered_price'] = consumerRequest.offered_price
                response_data['description'] = consumerRequest.description
                response_data['timestamp'] = consumerRequest.timestamp
                response_data['availability'] = consumerRequest.availability
                response_data['consumer'] = consumerRequest.consumer.pk
                if consumerRequest.accepted_producer != None:
                    response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
                else:
                    response_data['accepted_producer'] = None

            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)

        # The form filled with the consumer's data
        else:
            accepted_producer = None
            if consumerRequest.accepted_producer != None:
                accepted_producer = consumerRequest.accepted_producer.pk
            form = UpdateConsumerRequestForm(
                initial={'title': consumerRequest.title, 'offered_price': consumerRequest.offered_price,
                         'description': consumerRequest.description, 'timestamp': consumerRequest.timestamp,
                         'availability': consumerRequest.availability, 'consumer': consumerRequest.consumer.pk,
                         'accepted_producer': accepted_producer})
            return render(request, 'update_consumerRequest.html', {'form': form, 'update': True})

    except:
        response['ok'] = False

        response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def delete_consumerRequest(request, consumerRequest_pk):

    response = {}
    response_data = {}
    try:
        consumerRequest = ConsumerRequest.objects.get(pk=consumerRequest_pk)

        response['ok'] = True

        # Adding the deleted consumer's data to json response
        response_data['pk'] = consumerRequest.pk
        response_data['title'] = consumerRequest.title
        response_data['offered_price'] = consumerRequest.offered_price
        response_data['description'] = consumerRequest.description
        response_data['timestamp'] = consumerRequest.timestamp
        response_data['availability'] = consumerRequest.availability
        response_data['consumer'] = consumerRequest.consumer.pk

        if consumerRequest.accepted_producer != None:
            response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
        else:
            response_data['accepted_producer'] = None

        consumerRequest.delete()

    except:
        response['ok'] = False

    response['result'] = response_data
    return JsonResponse(response)

def getHighestPriceConsumerRequest(request):
    response = {}
    response_data = {}

    try:
        #Finds the highest priced consumer request that is not accepted by a producer
        consumerRequest = ConsumerRequest.objects.filter(accepted_producer__isnull = True).latest('offered_price')
        response_data['pk'] = consumerRequest.pk
        response_data['title'] = consumerRequest.title
        response_data['offered_price'] = consumerRequest.offered_price
        response_data['description'] = consumerRequest.description
        response_data['timestamp'] = consumerRequest.timestamp
        response_data['availability'] = consumerRequest.availability
        response_data['consumer'] = consumerRequest.consumer.pk

        if consumerRequest.accepted_producer != None:
            response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
        else:
            response_data['accepted_producer'] = None
        response['ok'] = True

    except:
        response['ok'] = False

    response['result'] = response_data

    return JsonResponse(response)

def getNewestConsumerRequest(request):
    response = {}
    response_data = {}

    try:
        #Finds the newest consumer request that is not accepted by a producer
        consumerRequest = ConsumerRequest.objects.filter(accepted_producer__isnull = True).last()
        response_data['pk'] = consumerRequest.pk
        response_data['title'] = consumerRequest.title
        response_data['offered_price'] = consumerRequest.offered_price
        response_data['description'] = consumerRequest.description
        response_data['timestamp'] = consumerRequest.timestamp
        response_data['availability'] = consumerRequest.availability
        response_data['consumer'] = consumerRequest.consumer.pk

        if consumerRequest.accepted_producer != None:
            response_data['accepted_producer'] = consumerRequest.accepted_producer.pk
        else:
            response_data['accepted_producer'] = None
        response['ok'] = True

    except:
        response['ok'] = False

    response['result'] = response_data

    return JsonResponse(response)

@csrf_exempt
def create_authenticator (request):
    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = CreateAuthenticatorForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Creating the authenticator based on form input
                auth_obj = Authenticator()
                auth_obj.user_id = form.cleaned_data['user_id']
                auth_obj.is_consumer = form.cleaned_data['is_consumer']

                #Check that user exists
                if auth_obj.is_consumer:
                    user = Consumer.objects.get(pk=auth_obj.user_id)
                else:
                    user = Producer.objects.get(pk=auth_obj.user_id)

                auth_obj.date_created = datetime.date.today().strftime("%B %d, %Y")
                unique = False
                while not unique:
                    auth = hmac.new(
                        key=settings.SECRET_KEY.encode('utf-8'),
                        msg=os.urandom(32),
                        digestmod='sha256',
                    ).hexdigest()

                    try:
                        a = Authenticator.objects.get(authenticator = auth)
                    except Authenticator.DoesNotExist:
                        unique = True

                auth_obj.authenticator = auth
                auth_obj.save()

                # Adding the created consumer's data to json response
                response_data['user_id'] = auth_obj.user_id
                response_data['is_consumer'] = auth_obj.is_consumer
                response_data['authenticator'] = auth_obj.authenticator
                response_data['date_created'] = auth_obj.date_created
            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)


        else:
            # An unfilled form gets displayed
            form = CreateAuthenticatorForm()
            return render(request, 'create_authenticator.html', {'form': form, 'title': 'Create Authenticator'})
    except:
        response['ok'] = False

        response['result'] = response_data


    return JsonResponse(response)

@csrf_exempt
def delete_authenticator(request):

    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = EnterAuthenticatorForm(request.POST)

            if form.is_valid():
                response['ok'] = True

                auth_obj = Authenticator.objects.get(authenticator=form.cleaned_data["authenticator"])
                response_data['user_id'] = auth_obj.user_id
                response_data['is_consumer'] = auth_obj.is_consumer
                response_data['authenticator'] = auth_obj.authenticator
                response_data['date_created'] = auth_obj.date_created

                auth_obj.delete()
            else:
                response['ok'] = False

        else:
            # An unfilled form gets displayed
            form = EnterAuthenticatorForm()
            return render(request, 'create_authenticator.html', {'form': form, 'title': 'Delete Authenticator'})
    except:
        response['ok'] = False

    response['result'] = response_data
    return JsonResponse(response)

@csrf_exempt
def login(request):
    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():

                response['ok'] = True

                # Creating the authenticator based on form input
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                is_consumer = form.cleaned_data['is_consumer']

                #Check that user with password exists
                if is_consumer:
                    user = Consumer.objects.get(username=username)
                else:
                    user = Producer.objects.get(username=username)
                if check_password(password, user.password):
                    user_id = user.pk

                    post_data = {'user_id': user_id, 'is_consumer': is_consumer}

                    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                    req = urllib.request.Request('http://localhost:8000/api/v1/authenticators/create', data=post_encoded, method='POST')

                    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                    resp = json.loads(resp_json)

                    if resp['ok']:
                        response['ok'] = True
                        # Adding the created authenticator's data to json response
                        response_data['result'] = resp['result']
                    else:
                        response['ok'] = False
                else:
                    response['ok'] = False
            else:
                response['ok'] = False

            response['result'] = response_data

            return JsonResponse(response)

        else:
            # An unfilled form gets displayed
            form = LoginForm()
            return render(request, 'create_authenticator.html', {'form': form, 'title': 'Login'})
    except:
        response['ok'] = False

        response['result'] = response_data


    return JsonResponse(response)

@csrf_exempt
def validate(request):

    response = {}
    response_data = {}
    try:
        if request.method == 'POST':
            form = EnterAuthenticatorForm(request.POST)

            if form.is_valid():

                auth_obj = Authenticator.objects.get(authenticator=form.cleaned_data["authenticator"])
                response['ok'] = True
                response_data['user_id'] = auth_obj.user_id
                response_data['is_consumer'] = auth_obj.is_consumer
                response_data['authenticator'] = auth_obj.authenticator
                response_data['date_created'] = auth_obj.date_created

            else:
                response['ok'] = False

        else:
            # An unfilled form gets displayed
            form = EnterAuthenticatorForm()
            return render(request, 'create_authenticator.html', {'form': form, 'title': 'Validate'})
    except:
        response['ok'] = False

    response['result'] = response_data
    return JsonResponse(response)