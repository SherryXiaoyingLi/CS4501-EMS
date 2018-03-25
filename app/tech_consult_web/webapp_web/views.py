from django.shortcuts import render
from .forms import LoginForm, CreateConsumerRequestForm, CreateConsumerForm, CreateProducerForm
from .forms import EnterAuthenticatorForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse

def index(request):
    logged_in = True
    auth = request.COOKIES.get('auth')
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    if not auth:
        logged_in = False

    #response = render(request, 'logout.html')
    #response.delete_cookie('auth')
    #response.delete_cookie('user_id')
    #response.delete_cookie('is_consumer')

    context_dict = {'newest_pk': 1, 'highest_pk': 1, 'logged_in':logged_in, 'is_consumer':is_consumer, 'username':username, 'msg':None}

    # make a GET request and parse the returned JSON
    # note, no timeouts, error handling or all the other things needed to do this for real
    print("About to perform the GET request...")

    req = urllib.request.Request('http://exp-api:8000/api/v1/getNewestRequestPk')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)

    if resp['ok']:

        context_dict['newest_pk'] = resp['result']['pk']

        req = urllib.request.Request('http://exp-api:8000/api/v1/getHighestRequestPk')

        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        print(resp)
        context_dict['highest_pk'] = resp['result']['pk']

    return render(request, "index.html", context_dict)

def request_detail(request, consumerRequest_pk):
    logged_in = True
    auth = request.COOKIES.get('auth')
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    if not auth:
        logged_in = False
    context_dict = {'title': 'New to AWS', 'description': 'Looking for someone to teach me AWS', 'offered_price': 75.0, 'timestamp': 'March 9, 2018.  7:55', 'availability': 'Mondays and Wednesdays', 'consumer_username': 'bob1', 'consumer_email': 'bob1@gmail.com', 'consumer_phone': '434-958-2913', 'producer_username': None}

    req = urllib.request.Request('http://exp-api:8000/api/v1/requestDetail/' + str(consumerRequest_pk))

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)

    if resp['ok']:

        context_dict['title'] = resp['result']['title']
        context_dict['description'] = resp['result']['description']
        context_dict['offered_price'] = resp['result']['offered_price']
        context_dict['timestamp'] = resp['result']['timestamp']
        context_dict['availability'] = resp['result']['availability']
        context_dict['consumer_username'] = resp['result']['consumer_username']
        context_dict['consumer_email'] = resp['result']['consumer_email']
        context_dict['consumer_phone'] = resp['result']['consumer_phone']
        context_dict['producer_username'] = resp['result']['producer_username']
        context_dict['logged_in'] = logged_in
        return render(request, "request_detail.html", context_dict)

    else:
        return HttpResponse("Consumer request does not exist.")


#for login page
#read login info, pass to log in exp srvc, receive authenticator back if password correct
#if successfully logged in, pass back cookie to browser
#if failed, return login failure response
def login (request):
 logged_in = True
 auth = request.COOKIES.get('auth')
 user_id = request.COOKIES.get('user_id')
 is_consumer = (request.COOKIES.get('is_consumer')=="True")
 if not auth:
    logged_in = False
 resultResp= {}
 response= {}
 try:
    if request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            #response['ok'] = True

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_consumer = form.cleaned_data['is_consumer']

            #username = "mylee3"
            #password = "ilikeseals"
            #is_consumer = True
            post_data = {'username': username, 'password': password, 'is_consumer': is_consumer}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

            # To do: implement django form and post in exp layer
            req = urllib.request.Request('http://exp-api:8000/api/v1/login',data=post_encoded,method='POST')
            #req = urllib.request.Request('http://exp-api:8000/api/v1/login')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            if resp['ok']:

                resultResp['authenticator'] = resp['result']['authenticator']
                resultResp['user_id'] = resp['result']['user_id']
                resultResp['is_consumer'] = resp['result']['is_consumer']
                #cookie_key =resultResp['authenticator']['user_id']
                cookie_value = resultResp['authenticator']
                next = reverse('index')
                try:
                 if request.GET['next']:
                        next = request.GET['next']
                except:
                    next = reverse('index')
                response = HttpResponseRedirect(next)
                # response = HttpResponseRedirect(next)

                #set cookie and use user_id as cookie key
                response.set_cookie(key="auth",value=cookie_value,path='/',domain=None)
                response.set_cookie(key="user_id",value=resultResp['user_id'],path='/',domain=None)
                response.set_cookie(key="is_consumer",value=is_consumer,path='/',domain=None)
                response.set_cookie(key="username", value=username, path='/', domain=None)
                #  resultResp['username'] = resp['result']['username']
                #response.set_cookie(key="username",value=resultResp['username'])

                return response
            else:
                return HttpResponse("Invalid credentials. Check your username and password or sign up first.")
        else:
            return HttpResponse("Log in validation failed. Please create account first.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form , 'logged_in':logged_in, 'auth':auth, 'user_id':user_id, 'is_consumer':is_consumer})
 except:
    return HttpResponse("Log in validation failed. Please create account first.")


def logout(request):
    #response = render(request, 'logout.html')
    #response.delete_cookie('auth')
    #response.delete_cookie('user_id')
    #response.delete_cookie('is_consumer')

 #this variable shows the current status of user
 logged_in = True
 auth = request.COOKIES.get('auth')
 #user_id = request.COOKIES.get('user_id')
 #is_consumer = request.COOKIES.get('is_consumer')
 #validate if the authenticator cookie was set before
 if not auth:
    logged_in = False
    return render(request, 'logout.html',{'logged_in':logged_in,'auth':auth})

 else:
    #delete cookie, authenticator

    resultResp= {}
    response= {}
    try:

            #post_data = {'authenticator': c2d8a3d1856c15218c99018f7965e5b8f88eda7a82c0c234bbf434adea6b918a}
            post_data = {'authenticator':auth}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

            req = urllib.request.Request('http://exp-api:8000/api/v1/logout',data=post_encoded,method='POST')
            #req = urllib.request.Request('http://exp-api:8000/api/v1/logout')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            if resp['ok']:

                response = render(request, 'logout.html',{'logged_in':True,'auth':auth})
                response.delete_cookie('auth')
                response.delete_cookie('user_id')
                response.delete_cookie('is_consumer')
                response.delete_cookie('username')
                return response
            else:
                return HttpResponse("Log out failed.")

    except:
        return HttpResponse("Log out failed.")

@csrf_exempt
def createListing(request):
     resultResp= {}
     response= {}
     # Try to get the authenticator cookie
     auth = request.COOKIES.get('auth')
     # If the authenticator cookie wasn't set...
     if not auth:
         # Handle user not logged in while trying to create a listing
         return HttpResponseRedirect(reverse("web_login") + "?next=" + reverse("web_create_listing"))
     is_consumer = (request.COOKIES.get('is_consumer')=="True")
     username = request.COOKIES.get('username')
     #if not is_consumer:
     #    return HttpResponse("You can only create a listing as a consumer.")
     #else:
     user_id = request.COOKIES.get('user_id')
     try:
        if request.method =='POST':
            form = CreateConsumerRequestForm(request.POST)

            if form.is_valid():

                #response['ok'] = True

                title = form.cleaned_data['title']
                offered_price = form.cleaned_data['offered_price']
                description = form.cleaned_data['description']
                availability = form.cleaned_data['availability']
                consumer = int(user_id)

                post_data = {'title': title, 'offered_price': offered_price, 'description': description, 'availability': availability, 'consumer':consumer, 'authenticator': auth}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/login',data=post_encoded,method='POST')
                req = urllib.request.Request('http://exp-api:8000/api/v1/createListing', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    pk=resp['result']['pk']
                    response = HttpResponseRedirect(reverse('web_request_detail', kwargs={'consumerRequest_pk':pk}))
                    return response
            else:
                return HttpResponse("Failed to create listing.")
        else:
            form = CreateConsumerRequestForm()
            return render(request, 'create_listing.html', {'form':form, 'is_consumer':is_consumer, 'username': username})
     except:
        return HttpResponse("Create listing failed.")

@csrf_exempt
def createConsumer(request):
    resultResp = {}
    response = {}
    logged_in = True
    auth = request.COOKIES.get('auth')
    if not auth:
        logged_in = False
    try:
        if request.method =='POST':
            form = CreateConsumerForm(request.POST)

            if form.is_valid():

                #response['ok'] = True

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']

                post_data = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email':email}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/login',data=post_encoded,method='POST')
                req = urllib.request.Request('http://exp-api:8000/api/v1/createConsumer', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    response = HttpResponseRedirect(reverse('index'))

                    return response
            else:
                return HttpResponse("Failed to create account.")
        else:
            form = CreateConsumerForm()
            return render(request, 'create_consumer.html', {'form':form, 'logged_in':logged_in})
    except:
        return HttpResponse("Create account failed.")

@csrf_exempt
def createProducer(request):
    resultResp = {}
    response = {}
    logged_in = True
    auth = request.COOKIES.get('auth')
    if not auth:
        logged_in = False
    try:
        if request.method =='POST':
            form = CreateProducerForm(request.POST)

            if form.is_valid():

                #response['ok'] = True

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                bio = form.cleaned_data['bio']
                skills = form.cleaned_data['skills']

                post_data = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email':email, 'bio': bio, 'skills':skills}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/login',data=post_encoded,method='POST')
                req = urllib.request.Request('http://exp-api:8000/api/v1/createProducer', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    response = render(request, "index.html")
                    return response
            else:
                return HttpResponse("Failed to create account.")
        else:
            form = CreateProducerForm()
            return render(request, 'create_producer.html', {'form':form, 'logged_in':logged_in})
    except:
        return HttpResponse("Create account failed.")
