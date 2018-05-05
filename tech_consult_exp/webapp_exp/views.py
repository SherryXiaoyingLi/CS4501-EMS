from django.shortcuts import render
from django.shortcuts import render_to_response
from .forms import LoginForm
from .forms import EnterAuthenticatorForm, CreateConsumerRequestForm, CreateConsumerForm, CreateProducerForm, SearchForm, SearchConsumerForm, SearchProducerForm, UpdateConsumerRequestForm, UpdateConsumerForm, UpdateProducerForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

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

                #Added for now to test in exp layer
                #results['ok'] = True
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
                        response_data['timestamp'] = results2['result']['timestamp']
                        response_data['availability'] = results2['result']['availability']
                        response_data['consumer'] = results2['result']['consumer']
                        response_data['accepted_producer'] = None
                        response_data['pk'] = results2['result']['pk']


                        producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
                        # Try to create KafkaProducer globally, otherwise it can be called inside function but would get destroyed each time

                        response_data['type']="listing"
                        # inside create_listing function
                        new_listing = response_data
                        #new_listing = {'title': 'Help with Kafka', 'offered_price': 50.0,
                        #           'description': 'New to Kafka, looking for someone to teach me',
                        #           'timestamp': 'March 29, 2018', 'availability': 'Mondays, Tuesdays, Wednesdays',
                        #           'consumer': 3, 'accepted_producer': 'null', 'pk': 10}

                        producer.send('kafka_topic', json.dumps(new_listing).encode('utf-8'))
                        producer.close()

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

                #Added for now to test in exp layer
                #results['ok'] = True

                if results['ok']:
                    response['ok'] = True
                    response_data['username'] = results['result']['username']
                    response_data['password'] = results['result']['password']
                    response_data['first_name'] = results['result']['first_name']
                    response_data['last_name'] = results['result']['last_name']
                    response_data['phone'] = results['result']['phone']
                    response_data['email'] = results['result']['email']
                    response_data['pk'] = results['result']['pk']

                    producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
                    # Try to create KafkaProducer globally, otherwise it can be called inside function but would get destroyed each time

                    # inside create_consumer function
                    response_data['type']="consumer"
                    new_consumer = response_data
                    #new_consumer = {'username':'XYL','passowrd':'abc950312','first_name':'Xiaoying','last_name':'Li','phone':'434122','email':'kqqq@126.com','pk'=3}
                    producer.send('kafka_topic',json.dumps(new_consumer).encode('utf-8'))
                    producer.close()

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

                #Added for now to test in exp layer
                #results['ok'] = True

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

                    producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
                    # Try to create KafkaProducer globally, otherwise it can be called inside function but would get destroyed each time

                    # inside create_consumer function
                    response_data['type']="producer"
                    new_producer = response_data
                    #new_producer = {'username':'Xxx','passowrd':'abc950312','first_name':'Xiaoying','last_name':'Li','phone':'4341221','email':'kqqq@12611.com','pk'=4}
                    producer.send('kafka_topic',json.dumps(new_producer).encode('utf-8'))
                    producer.close()
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

@csrf_exempt
def search(request):
    response = {}
    response_data = []

    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)

            if form.is_valid():
                response["ok"] = True
                query = form.cleaned_data['query']

                #Will call elastic search with query
                es = Elasticsearch(['es'])
                results = es.search(index='listing_index',
                                    body={'query': {'query_string': {'query': query}}, 'size': 10})
                #print(results['hits']['hits'][0]['_source'])
                results = results['hits']['hits']
                for r in results:
                    data = r['_source']
                    consumer_pk = data['consumer']
                    req = urllib.request.Request('http://models-api:8000/api/v1/consumers/' + str(consumer_pk))
                    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                    results = json.loads(resp_json)
                    consumer_username = results['result']['username']
                    data['consumer_username'] = consumer_username
                    #data['consumer_pk'] = consumer_pk
                    response_data.append(data)

            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to search form in the experience layer."
        else:
            form = SearchForm()
            return render(request, 'search.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with search in the experience layer"
    response["result"] = response_data
    return JsonResponse(response)

# Update a listing
@csrf_exempt
def updateListing(request, consumerRequest_pk):
    response = {}
    response_data= {}

    try:
        if request.method == 'POST':
            form = UpdateConsumerRequestForm(request.POST)

            if form.is_valid():
                '''
                title = 'hiya'
                offered_price = 2.0
                description = 'stuff'
                availability = 'yeah'
                consumer = 1
                accepted_producer = 0
                '''

                #Added for now to test in exp layer
                #results['ok'] = True
                response["ok"] = True
                post_data = {}

                if form.cleaned_data['title']:
                    title = form.cleaned_data['title']
                    post_data['title'] = title
                if form.cleaned_data['offered_price']:
                    offered_price = float(form.cleaned_data['offered_price'])
                    post_data['offered_price'] = offered_price
                if form.cleaned_data['description']:
                    description = form.cleaned_data['description']
                    post_data['description'] = description
                if form.cleaned_data['availability']:
                    availability = form.cleaned_data['availability']
                    post_data['availability'] = availability
                if form.cleaned_data['consumer']:
                    consumer = int(form.cleaned_data['consumer'])
                    post_data['consumer'] = consumer
                accepted_producer = None

                # post_data = {'title':title, 'offered_price':offered_price, 'description': description, 'availability':availability, 'consumer':consumer}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                req = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/'+ str(consumerRequest_pk)+'/update', data=post_encoded,method='POST') #data???
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                results = json.loads(resp_json)

                if results['ok']:
                    response['ok'] = True
                    response_data['title'] = results['result']['title']
                    response_data['offered_price'] = results['result']['offered_price']
                    response_data['description'] = results['result']['description']
                    response_data['timestamp'] = results['result']['timestamp']
                    response_data['availability'] = results['result']['availability']
                    response_data['consumer'] = results['result']['consumer']
                    response_data['accepted_producer'] = None
                    response_data['pk'] = results['result']['pk']

                else:
                    response['ok'] = False
                    response['msg'] = "Error with creating listing in the experience layer."
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form in the experience layer."
        else:
            form = UpdateConsumerRequestForm()
            return render(request, 'update_consumer_request.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with updating listing in the exp layer."

    response['result'] = response_data
    return JsonResponse(response)

# Update a consumer
@csrf_exempt
def updateConsumer(request, consumer_pk):
    response = {}
    response_data = {}
    try:
        # User submits the form's data
        if request.method == 'POST':
            form = UpdateConsumerForm(request.POST)

            if form.is_valid():
                response["ok"] = True
                post_data = {}
                if form.cleaned_data['username']:
                    username = form.cleaned_data['username']
                    post_data['username'] = username
                if form.cleaned_data['password']:
                    password = form.cleaned_data['password']
                    #password = make_password(password, salt=None, hasher='default')
                    post_data['password'] = password
                if form.cleaned_data['first_name']:
                    first_name = form.cleaned_data['first_name']
                    post_data['first_name'] = first_name
                if form.cleaned_data['last_name']:
                    last_name = form.cleaned_data['last_name']
                    post_data['last_name'] = last_name
                if form.cleaned_data['phone']:
                    phone = form.cleaned_data['phone']
                    post_data['phone'] = phone
                if form.cleaned_data['email']:
                    email = form.cleaned_data['email']
                    post_data['email'] = email

                #post_data['pk'] = producer_pk
                #post_data = {'password':password, 'first_name': first_name, 'last_name':last_name, 'phone':phone, 'email':email}
                #post_data = {'email':'a@gmail.com'}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                req = urllib.request.Request('http://models-api:8000/api/v1/consumers/'+ str(consumer_pk)+'/update', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    response_data = resp['result']
                else:
                    response['ok'] = False
                    response['msg'] = "Fail to update consumer profile in experience layer."
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form."

        else:
            form = UpdateConsumerForm()
            return render(request, 'update_consumer.html', {'form': form})
    except:
        response['ok'] = False
        response['msg'] = "Error with updating producer."

    response['result'] = response_data
    return JsonResponse(response)


# Update a producer
@csrf_exempt
def updateProducer(request, producer_pk):
    response = {}
    response_data = {}
    try:
        # User submits the form's data
        if request.method == 'POST':
            form = UpdateProducerForm(request.POST)

            if form.is_valid():
                  response["ok"] = True
                  post_data={}
                  if form.cleaned_data['username']:
                    username = form.cleaned_data['username']
                    post_data['username'] = username
                  if form.cleaned_data['password']:
                    password = form.cleaned_data['password']
                    #password = make_password(password, salt=None, hasher='default')
                    post_data['password'] = password
                  if form.cleaned_data['first_name']:
                     first_name = form.cleaned_data['first_name']
                     post_data['first_name'] = first_name
                  if form.cleaned_data['last_name']:
                     last_name = form.cleaned_data['last_name']
                     post_data['last_name'] = last_name
                  if form.cleaned_data['phone']:
                     phone = form.cleaned_data['phone']
                     post_data['phone'] = phone
                  if form.cleaned_data['email']:
                     email = form.cleaned_data['email']
                     post_data['email'] = email
                  if form.cleaned_data['bio']:
                     bio = form.cleaned_data['bio']
                     post_data['bio'] = bio
                  if form.cleaned_data['skills']:
                     skills = form.cleaned_data['skills']
                     post_data['skills'] = skills

                  #post_data['pk'] = producer_pk
                  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                  req = urllib.request.Request('http://models-api:8000/api/v1/producers/'+ str(producer_pk)+'/update', data=post_encoded,method='POST')
                  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                  resp = json.loads(resp_json)

                  if resp['ok']:
                      response_data = resp['result']
                  else:
                      response['ok'] = False
                      response['msg'] = "Fail to update producer profile in experience layer."
            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to form."

            response['result'] = response_data
            return JsonResponse(response)

        else:
            form = UpdateProducerForm()
            return render(request, 'update_producer.html', {'form': form, 'update': True})
    except:
        response['ok'] = False
        response['msg'] = "Error with updating producer."

    response['result'] = response_data
    return JsonResponse(response)


# search for consumers
@csrf_exempt
def searchConsumer(request):
 response = {}
 response_data = []
 try:
    if request.method == 'POST':
        form = SearchConsumerForm(request.POST)
        
        if form.is_valid():
            response["ok"] = True
            query = form.cleaned_data['query']
            
            #Will call elastic search with query
            es = Elasticsearch(['es'])
            results = es.search(index='consumer_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
            results = results['hits']['hits']
            
            for r in results:
                data = r['_source']
                response_data.append(data)

            #response_data=results
        else:
            response['ok'] = False
            response['msg'] = "Invalid data sent to search form in the experience layer."
    
    else:
        form = SearchConsumerForm()
        return render(request, 'searchConsumer.html', {'form': form})
 except:
    response["ok"] = False
    response['msg'] = "Error with search in the experience layer"
 response["result"] = response_data
 return JsonResponse(response)

# search for producers
@csrf_exempt
def searchProducer(request):
    response = {}
    response_data = []

    try:
        if request.method == 'POST':
            form = SearchProducerForm(request.POST)

            if form.is_valid():
                response["ok"] = True
                query = form.cleaned_data['query']

                #Will call elastic search with query
                es = Elasticsearch(['es'])
                results = es.search(index='producer_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
                results = results['hits']['hits']
                for r in results:
                    data = r['_source']
                    response_data.append(data)

            else:
                response['ok'] = False
                response['msg'] = "Invalid data sent to search form in the experience layer."
        else:
                    form = SearchProducerForm()
                    return render(request, 'searchProducer.html', {'form': form})
    except:
        response["ok"] = False
        response['msg'] = "Error with search in the experience layer"
    response["result"] = response_data
    return JsonResponse(response)

# render recommendation details
@csrf_exempt
def get_recommendations (request, consumerRequest_pk) :
    response = {}
    response_data = {}
    
    if request.method == 'GET' :
        try:
            req = urllib.request.Request('http://models-api:8000/api/v1/recommendations/'+ str(consumerRequest_pk))
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            results = json.loads(resp_json)

            if results['ok']:
                recommended_items = results["result"]["recommended_items"]
                recommended_data = []
                for item_pk in recommended_items:
                    req_item = urllib.request.Request('http://models-api:8000/api/v1/consumerRequests/' + str(item_pk))
                    resp_json_item = urllib.request.urlopen(req_item).read().decode('utf-8')
                    results_item = json.loads(resp_json_item)
                    title = results_item['result']['title']
                    description = results_item['result']['description']
                    consumer_pk = results_item['result']['consumer']
                    # get consumer name and id for recommended items
                    req_username = urllib.request.Request('http://models-api:8000/api/v1/consumers/' + str(consumer_pk))
                    resp_json_username = urllib.request.urlopen(req_username).read().decode('utf-8')
                    results_username = json.loads(resp_json_username)
                    consumerName = results_username['result']['username']
                    data={'item_id':item_pk,'consumerName':consumerName, 'consumer':consumer_pk,'title':title, 'description':description}
                    recommended_data.append(data)
                
                item_id = results["result"]["item_id"]
                response["ok"] = True
                response_data["recommendations"] = recommended_data
                response_data["item_id"] = item_id
            else:
                response["ok"] = False
                response['msg'] = "Recommendations may not exist."
        except:
                response["ok"] = False
                response['msg'] = "Error occurred at experience layer when getting recommendations."
    
        response['result'] = response_data
        return JsonResponse(response)
    else:
        response["ok"] = False
        response['msg'] = "Error request method type, should be GET."
        return JsonResponse(response)




