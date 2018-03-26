from django.shortcuts import render
from django.shortcuts import render_to_response
from .forms import LoginForm
from .forms import EnterAuthenticatorForm, CreateConsumerRequestForm, CreateConsumerForm, CreateProducerForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import urllib.request
import urllib.parse
import json

def index(request):

    return HttpResponse("CS4501 Project 3, Experience layer")

# For index page
# Returns the pk of the newest consumer request
def getNewestRequestPk(request):
    response = {}
    response_data = {}
    try:
        req = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/getNewest')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok'] == True:
            newest_pk = results["result"]["pk"]
            response["ok"] = True
            response_data["pk"] = newest_pk
        else:
            response["ok"] = False
    except:
        response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)

# For index page
# Returns the pk of the consumer request with the highest price
def getHighestRequestPk(request):
    response = {}
    response_data = {}
    try:
        req = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/getHighestPrice')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok'] == True:
            newest_pk = results["result"]["pk"]
            response["ok"] = True
            response_data["pk"] = newest_pk
        else:
            response["ok"] = False
    except:
        response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)

# For request detail page
# Returns the request information, consumer information, and producer username
def getRequestDetail(request, consumerRequest_pk):
    response = {}
    response_data = {}

    try:

        req = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/' + str(consumerRequest_pk))
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok'] == True:
            consumer_pk = results['result']['consumer']
            req2 = urllib.request.Request('http://models-api:8000/api/v1/consumers/' + str(consumer_pk))
            resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
            results2 = json.loads(resp_json2)
            # consumer_username = results2['result']['username']

            response['ok'] = True

            response_data['title'] = results['result']['title']
            response_data['description'] = results['result']['description']
            response_data['offered_price'] = results['result']['offered_price']
            response_data['timestamp'] = results['result']['timestamp']
            response_data['availability'] = results['result']['availability']
            response_data['consumer_pk'] = consumer_pk
            response_data['consumer_username'] = results2['result']['username']
            response_data['consumer_email'] = results2['result']['email']
            response_data['consumer_phone'] = results2['result']['phone']

            accepted_producer = results['result']['accepted_producer']
            if accepted_producer != None:
                req3 = urllib.request.Request('http://models-api:8000/api/v1/producers/' + str(accepted_producer))
                resp_json3 = urllib.request.urlopen(req3).read().decode('utf-8')
                results3 = json.loads(resp_json3)
                response_data['producer_username'] = results3['result']['username']
                response_data['producer_pk'] = results3['result']['pk']
            else:
                response_data['producer_username'] = None

        else:
            response['ok'] = False
    except:
        response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)

# For consumer detail page
# Returns the consumer's informatopn
def getConsumerDetail(request, consumer_pk):
    response = {}
    response_data = {}

    try:

        req = urllib.request.Request('http://models-api:8000/api/v1/consumers/' + str(consumer_pk))
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok'] == True:
            response['ok'] = True
            response_data['consumer_username'] = results['result']['username']
            response_data['full_name'] = results['result']['first_name'] + " " + results['result']['last_name']
            response_data['email'] = results['result']['email']
            response_data['phone'] = results['result']['phone']

        else:
            response['ok'] = False
    except:
        response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)

# For producer detail page
# Returns the consumer's informatopn
def getProducerDetail(request, producer_pk):
    response = {}
    response_data = {}

    try:

        req = urllib.request.Request('http://models-api:8000/api/v1/producers/' + str(producer_pk))
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok'] == True:
            response['ok'] = True
            response_data['producer_username'] = results['result']['username']
            response_data['full_name'] = results['result']['first_name'] + " " + results['result']['last_name']
            response_data['email'] = results['result']['email']
            response_data['phone'] = results['result']['phone']
            response_data['bio'] = results['result']['bio']
            response_data['skills'] = results['result']['skills']

        else:
            response['ok'] = False
    except:
        response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)

#Login authenticator
#Take a username and password from client(web f.e/mobile app, etc)
#Return an authenticator(passed from model API) back to client if user password correct
@csrf_exempt
def login(request):
  response = {}
  response_data= {}

  try:
   if request.method =='POST':
     form = LoginForm(request.POST)

     if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        is_consumer = form.cleaned_data['is_consumer']

        #calling model API views.login, get an authenticator back if username and password correct
        #username = "mylee3"
        #password = "ilikeseals"
        #is_consumer = True
        post_data = {'username': username, 'password': password, 'is_consumer': is_consumer}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/login', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        results = json.loads(resp_json)

        if results['ok']:

            response_data['authenticator'] = results['result']['authenticator']
            response_data['user_id'] = results['result']['user_id']
            response_data['is_consumer'] = results['result']['is_consumer']

            response['ok'] = True

        else:
            response['ok'] = False
     else:
        response['ok'] = False
   else:
       form = LoginForm()
       return render(request, 'login.html', {'form':form})

  except:
        response["ok"] = False

  response['result'] = response_data
  return JsonResponse(response)

@csrf_exempt
def logout(request):
    response = {}
    response_data= {}
    try:
       if request.method =='POST':
           form = EnterAuthenticatorForm(request.POST)
           if form.is_valid():
              authenticator = form.cleaned_data['authenticator']
              post_data={'authenticator':authenticator}
              post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
              req = urllib.request.Request('http://models-api:8000/api/v1/authenticators/delete', data=post_encoded, method='POST')
              resp_json = urllib.request.urlopen(req).read().decode('utf-8')
              results = json.loads(resp_json)
              if results['ok']:
                      response_data['authenticator'] = authenticator
                      response['ok'] = True
              else:
                      response['ok'] = False
           else:
               response['ok'] = False
       else:
           form = EnterAuthenticatorForm()
           return render(request, 'logout.html', {'form':form})
    except:
           response["ok"] = False

    response['result'] = response_data
    return JsonResponse(response)


@csrf_exempt
def createListing(request):
    response = {}
    response_data= {}

    try:
        if request.method == 'POST':
            form = CreateConsumerRequestForm(request.POST)

            if form.is_valid():
                '''
                title = 'hiya'
                offered_price = 2.0
                description = 'stuff'
                availability = 'yeah'
                consumer = 1
                accepted_producer = 0
                '''
                auth = form.cleaned_data['authenticator']
                #validate the authenticator
                post_data = {'authenticator': auth}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                req = urllib.request.Request('http://models-api:8000/api/v1/authenticators/validate', data=post_encoded,
                                             method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                results = json.loads(resp_json)

                if results['ok']:
                    title = form.cleaned_data['title']
                    offered_price = float(form.cleaned_data['offered_price'])
                    description = form.cleaned_data['description']
                    availability = form.cleaned_data['availability']
                    consumer = int(form.cleaned_data['consumer'])
                    accepted_producer = None

                    post_data = {'title':title, 'offered_price':offered_price, 'description': description, 'availability':availability, 'consumer':consumer}
                    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                    req = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/create', data=post_encoded, method='POST') #data???
                    resp_json2 = urllib.request.urlopen(req).read().decode('utf-8')
                    results2 = json.loads(resp_json2)

                    if results2['ok']:
                        response['ok'] = True
                        response_data['title'] = results2['result']['title']
                        response_data['offered_price'] = results2['result']['offered_price']
                        response_data['description'] = results2['result']['description']
                        response_data['availability'] = results2['result']['availability']
                        response_data['consumer'] = results2['result']['consumer']
                        response_data['accepted_producer'] = None
                        response_data['pk'] = results2['result']['pk']
                    else:
                        response['ok'] = False
                        response['msg'] = "Error with creating listing in the experience layer."
                else:
                    response['ok'] = False
                    response['msg'] = "Invalid authenticator."
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form in the experience layer."
        else:
            form = CreateConsumerRequestForm()
            return render(request, 'create_consumer_request.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with creating listing in the exp layer."

    response['result'] = response_data
    return JsonResponse(response)

@csrf_exempt
def createConsumer(request):
    response = {}
    response_data= {}

    try:
        if request.method == 'POST':
            form = CreateConsumerForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']

                post_data = {'username':username, 'password':password, 'first_name': first_name, 'last_name':last_name, 'phone':phone, 'email': email}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                req = urllib.request.Request('http://models-api:8000/api/v1/consumers/create', data=post_encoded, method='POST') #data???
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                results = json.loads(resp_json)

                if results['ok']:
                    response['ok'] = True
                    response_data['username'] = results['result']['username']
                    response_data['password'] = results['result']['password']
                    response_data['first_name'] = results['result']['first_name']
                    response_data['last_name'] = results['result']['last_name']
                    response_data['phone'] = results['result']['phone']
                    response_data['email'] = results['result']['email']
                    response_data['pk'] = results['result']['pk']
                else:
                    response['ok'] = False
                    response['msg'] = results['msg']
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form in the experience layer."
        else:
            form = CreateConsumerForm()
            return render(request, 'create_consumer.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with creating consumer in the experience layer"

    response['result'] = response_data
    return JsonResponse(response)

@csrf_exempt
def createProducer(request):
    response = {}
    response_data= {}

    try:
        if request.method == 'POST':
            form = CreateProducerForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                bio = form.cleaned_data['bio']
                skills = form.cleaned_data['skills']

                post_data = {'username':username, 'password':password, 'first_name': first_name, 'last_name':last_name, 'phone':phone, 'email':email, 'bio':bio, 'skills':skills}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                req = urllib.request.Request('http://models-api:8000/api/v1/producers/create', data=post_encoded, method='POST') #data???
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                results = json.loads(resp_json)

                if results['ok']:
                    response['ok'] = True
                    response_data['username'] = results['result']['username']
                    response_data['password'] = results['result']['password']
                    response_data['first_name'] = results['result']['first_name']
                    response_data['last_name'] = results['result']['last_name']
                    response_data['phone'] = results['result']['phone']
                    response_data['email'] = results['result']['email']
                    response_data['bio'] = results['result']['bio']
                    response_data['skills'] = results['result']['skills']
                    response_data['pk'] = results['result']['pk']
                else:
                    response['ok'] = False
                    response['msg'] = results['msg']
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form in the experience layer."
        else:
            form = CreateProducerForm()
            return render(request, 'create_producer.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with creating producer in the experience layer"
    response['result'] = response_data
    return JsonResponse(response)
