from django.shortcuts import render
from .forms import LoginForm, CreateConsumerRequestForm, CreateConsumerForm, CreateProducerForm, SearchForm, SearchConsumerForm, SearchProducerForm, UpdateConsumerRequestForm, UpdateConsumerForm,UpdateProducerForm
from .forms import EnterAuthenticatorForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

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

    context_dict = {'newest_pk': 1, 'highest_pk': 1, 'logged_in':logged_in, 'is_consumer':is_consumer, 'username':username, 'user_id':user_id, 'msg':None}

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

    post_data = {'user_id':user_id, 'item_id':consumerRequest_pk}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

    # To do: implement django form and post in exp layer
    req2 = urllib.request.Request('http://exp-api:8000/api/v1/itemClick', data=post_encoded,method='POST')
    resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
    resp2 = json.loads(resp_json2)

    if resp['ok']:
        context_dict['ok'] = True
        context_dict['title'] = resp['result']['title']
        context_dict['description'] = resp['result']['description']
        context_dict['offered_price'] = resp['result']['offered_price']
        context_dict['timestamp'] = resp['result']['timestamp']
        context_dict['availability'] = resp['result']['availability']
        context_dict['consumer_pk'] = resp['result']['consumer_pk']
        context_dict['consumer_username'] = resp['result']['consumer_username']
        context_dict['consumer_email'] = resp['result']['consumer_email']
        context_dict['consumer_phone'] = resp['result']['consumer_phone']
        context_dict['producer_username'] = resp['result']['producer_username']
        if context_dict['producer_username']:
            context_dict['producer_pk'] = resp['result']['producer_pk']
        context_dict['logged_in'] = logged_in
        context_dict['username'] = username
        context_dict['is_consumer'] = is_consumer
        context_dict['user_id'] = user_id

        # get recommendations for the current listing
        req_recommendations = urllib.request.Request('http://exp-api:8000/api/v1/recommendations/' + str(consumerRequest_pk))
        resp_json_recommendations = urllib.request.urlopen(req_recommendations).read().decode('utf-8')
        results_recommendations = json.loads(resp_json_recommendations)

        if results_recommendations['ok']:
                recommended_items = results_recommendations["result"]["recommendations"]
                context_dict['recommendations'] = recommended_items

        return render(request, "request_detail.html", context_dict)

    else:
        context_dict['ok'] = False
        context_dict['msg'] = "Listing does not exist."
        return render(request, "request_detail.html", context_dict)

def consumer_detail(request, consumer_pk):
    logged_in = True
    auth = request.COOKIES.get('auth')
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    if not auth:
        logged_in = False
    context_dict = {'username': 'Marissa', 'full_name': 'Marissa Lee',
                    'email': "myl2vu@virginia.edu", 'phone': '434-958-2913'}

    req = urllib.request.Request('http://exp-api:8000/api/v1/consumerDetail/' + str(consumer_pk))

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)

    if resp['ok']:
        context_dict['ok'] = True
        context_dict['consumer_username'] = resp['result']['consumer_username']
        context_dict['full_name'] = resp['result']['full_name']
        context_dict['email'] = resp['result']['email']
        context_dict['phone'] = resp['result']['phone']
        context_dict['logged_in'] = logged_in
        context_dict['username'] = username
        context_dict['user_id'] = user_id
        context_dict['is_consumer'] = is_consumer

    else:
        context_dict['ok'] = False
        context_dict['msg'] = "Consumer does not exist."
    return render(request, "consumer_detail.html", context_dict)

def producer_detail(request, producer_pk):
    logged_in = True
    auth = request.COOKIES.get('auth')
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    if not auth:
        logged_in = False
    context_dict = {'username': 'Marissa', 'full_name': 'Marissa Lee',
                    'email': "myl2vu@virginia.edu", 'phone': '434-958-2913', 'bio':'I am a student', 'skills': 'Django, AWS'}

    req = urllib.request.Request('http://exp-api:8000/api/v1/producerDetail/' + str(producer_pk))

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)

    if resp['ok']:
        context_dict['ok']=True
        context_dict['producer_username'] = resp['result']['producer_username']
        context_dict['full_name'] = resp['result']['full_name']
        context_dict['email'] = resp['result']['email']
        context_dict['phone'] = resp['result']['phone']
        context_dict['bio'] = resp['result']['bio']
        context_dict['skills'] = resp['result']['skills']
        context_dict['logged_in'] = logged_in
        context_dict['username'] = username
        context_dict['user_id'] = user_id
        context_dict['is_consumer'] = is_consumer
    else:
        context_dict['ok'] = False
        context_dict['msg'] = "Producer does not exist."
    return render(request, "producer_detail.html", context_dict)

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

                #Using django messages based on https://stackoverflow.com/questions/1463489/how-do-i-pass-template-context-information-when-using-httpresponseredirect-in-dj
                messages.success(request, "You successfully logged in!")
                #set cookie and use user_id as cookie key
                response.set_cookie(key="auth",value=cookie_value,path='/',domain=None)
                response.set_cookie(key="user_id",value=resultResp['user_id'],path='/',domain=None)
                response.set_cookie(key="is_consumer",value=is_consumer,path='/',domain=None)
                response.set_cookie(key="username", value=username, path='/', domain=None)
                #  resultResp['username'] = resp['result']['username']
                #response.set_cookie(key="username",value=resultResp['username'])

                return response
            else:
                response = HttpResponseRedirect(reverse("web_login"))
                messages.error(request, "Invalid credentials. Check your username and password or sign up first.")
                return response
        else:
            response = HttpResponseRedirect(reverse("web_login"))
            messages.error(request, "Invalid credentials. Check your username and password or sign up first.")
            return response
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form , 'logged_in':logged_in, 'auth':auth, 'user_id':user_id, 'is_consumer':is_consumer})
 except:
     response = HttpResponseRedirect(reverse("web_login"))
     messages.error(request, "Invalid credentials. Check your username and password or sign up first.")
     return response


def logout(request):


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
                req = urllib.request.Request('http://exp-api:8000/api/v1/createListing', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    pk=resp['result']['pk']
                    response = HttpResponseRedirect(reverse('web_request_detail', kwargs={'consumerRequest_pk':pk}))
                    messages.success(request, "You successfully created a listing.")
                    return response
                else:
                    response = HttpResponseRedirect(reverse('web_create_listing'))
                    messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_listing'))
                messages.error(request, "Invalid data sent to form in the frontend.")
                return response
        else:
            form = CreateConsumerRequestForm()
            return render(request, 'create_listing.html', {'form':form, 'is_consumer':is_consumer, 'username': username})
     except:
         response = HttpResponseRedirect(reverse('web_create_listing'))
         messages.error(request, "Error with creating listing in the frontend.")
         return response

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
                    pk = resp['result']['pk']
                    response = HttpResponseRedirect(reverse('web_consumer_detail', kwargs={'consumer_pk': pk}))
                    messages.success(request, "You successfully created a consumer account.")
                    return response
                else:
                    response = HttpResponseRedirect(reverse('web_create_consumer'))
                    messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_consumer'))
                messages.error(request, "Invalid data sent to form in web layer.")
                return response
        else:
            form = CreateConsumerForm()
            return render(request, 'create_consumer.html', {'form':form, 'logged_in':logged_in})
    except:
        response = HttpResponseRedirect(reverse('web_create_consumer'))
        messages.error(request, "Error with creating new consumer account.")
        return response

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
                req = urllib.request.Request('http://exp-api:8000/api/v1/createProducer', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    pk = resp['result']['pk']
                    response = HttpResponseRedirect(reverse('web_producer_detail', kwargs={'producer_pk': pk}))
                    messages.success(request, "You successfully created a producer account.")
                    return response
                else:
                    response = HttpResponseRedirect(reverse('web_create_producer'))
                    messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_producer'))
                messages.error(request, "Invalid data sent to form in frontend.")
                return response
        else:
            form = CreateProducerForm()
            return render(request, 'create_producer.html', {'form':form, 'logged_in':logged_in})
    except:
        response = HttpResponseRedirect(reverse('web_create_producer'))
        messages.error(request, "Error with creating new producer account.")
        return response

@csrf_exempt
def searchResults(request):
    logged_in = True
    auth = request.COOKIES.get('auth')
    if not auth:
        logged_in = False
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    try:
        if request.method =='POST':
            form = SearchForm(request.POST)

            if form.is_valid():

                #response['ok'] = True

                query = form.cleaned_data['query']

                post_data = {'query': query}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/search')
                req = urllib.request.Request('http://exp-api:8000/api/v1/search', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    #pk = resp['result']['pk']
                    results = resp['result']
                    #results = [{'title': 'Help with docker', 'description': 'Looking for someone with experience', 'consumer_username': 'mylee3', 'consumer_pk': 1, 'timestamp': 'April 2, 2018', 'pk':1}]
                    return render(request, 'search_results.html',
                                  {'form': form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in': logged_in, 'query': query, 'results': results})

                else:
                    response = HttpResponseRedirect(reverse('web_search_results'))
                    #messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_producer'))
                messages.error(request, "Invalid data sent to form in frontend.")
                return response
        else:
            form = SearchForm()
            return render(request, 'search_results.html', {'form':form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in':logged_in, 'query': '', 'results': None})
    except:
        response = HttpResponseRedirect(reverse('web_search_results'))
        messages.error(request, "Error with search.")
        return response

@csrf_exempt
def updateListing(request, consumerRequest_pk):
    logged_in = True
    # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')
    # If the authenticator cookie wasn't set...
    if not auth:
        logged_in = False
    is_consumer = (request.COOKIES.get('is_consumer')=="True")
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')

    response = {}
    response_data = {}
    try:
        # User submits the form's data
        if request.method == 'POST':
            form = UpdateConsumerRequestForm(request.POST)
            if form.is_valid():
                post_data={}
                # Updating the producer based on form input, only for newly inputed fields
                if form.cleaned_data['title']:
                    title = form.cleaned_data['title']
                    post_data['title'] = title
                if form.cleaned_data['offered_price']:
                    offered_price = form.cleaned_data['offered_price']
                    post_data['offered_price'] = offered_price
                if form.cleaned_data['description']:
                    description = form.cleaned_data['description']
                    post_data['description'] = description
                if form.cleaned_data['availability']:
                    availability = form.cleaned_data['availability']
                    post_data['availability'] = availability
                if user_id:
                    post_data['consumer'] = int(user_id)
                #post_data['email'] = "SherryLi@gmail.com"
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                req = urllib.request.Request('http://exp-api:8000/api/v1/updateListing/'+ str(consumerRequest_pk), data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)
                if resp['ok']:
                    #response_data = resp['result']
                    response = HttpResponseRedirect(reverse('web_request_detail', kwargs={'consumerRequest_pk': consumerRequest_pk}))
                    messages.success(request, "You successfully updated your listing.")
                    return response
                else:
                    response['msg'] = "Fail to update listing."
            else:
                response['msg'] = "Invalid data sent to form."

            response['result'] = response_data
            return JsonResponse(response)
        # The form without producer's data filled in
        else:
            form = UpdateConsumerRequestForm()
            return render(request, 'update_consumer_request.html', {'form': form, 'logged_in':logged_in, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username})
    except:
        response['msg'] = "Error with updating listing."

    response['result'] = response_data
    return JsonResponse(response)


@csrf_exempt
def updateConsumer(request, consumer_pk):
        logged_in = True
        # Try to get the authenticator cookie
        auth = request.COOKIES.get('auth')
        # If the authenticator cookie wasn't set...
        if not auth:
            logged_in = False
        is_consumer = (request.COOKIES.get('is_consumer') == "True")
        username = request.COOKIES.get('username')
        user_id = request.COOKIES.get('user_id')

        # check if logged in user_id same as producer_pk
        if user_id == consumer_pk:
            response = {}
            response_data = {}
            try:

                # User submits the form's data
                if request.method == 'POST':
                    form = UpdateConsumerForm(request.POST)

                    if form.is_valid():
                        post_data={}
                        # Updating the producer based on form input, only for newly inputed fields
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

                        #post_data['email'] = "SherryLi@gmail.com"
                        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
                        req = urllib.request.Request('http://exp-api:8000/api/v1/updateConsumer/'+ str(consumer_pk), data=post_encoded,method='POST')
                        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                        resp = json.loads(resp_json)

                        if resp['ok']:
                              #response_data = resp['result']
                              response = HttpResponseRedirect(reverse('web_consumer_detail', kwargs={'consumer_pk': consumer_pk}))
                              messages.success(request, "You successfully updated your consumer account.")
                              return response
                        else:
                             response['msg'] = "Fail to update producer profile."

                    else:
                          response['msg'] = "Invalid data sent to form."

                    response['result'] = response_data
                    return JsonResponse(response)
                # The form without producer's data filled in
                else:
                    form = UpdateConsumerForm()
                    return render(request, 'update_consumer.html', {'form': form, 'logged_in':logged_in, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username})
            except:
                   response['msg'] = "Error with updating producer."
        else:
                 response['msg'] = "Unidentified user. Please log in first."
        response['result'] = response_data
        return JsonResponse(response)




@csrf_exempt
def updateProducer(request, producer_pk):
 logged_in = True
 # Try to get the authenticator cookie
 auth = request.COOKIES.get('auth')
 # If the authenticator cookie wasn't set...
 if not auth:
     logged_in = False
 is_consumer = (request.COOKIES.get('is_consumer') == "True") # should change to false??
 username = request.COOKIES.get('username')
 user_id = request.COOKIES.get('user_id')

 # check if logged in user_id same as producer_pk
 if user_id == producer_pk:
    response = {}
    response_data = {}
    try:
        #producer = Producer.objects.get(pk=producer_pk)

        # User submits the form's data
        if request.method == 'POST':
            form = UpdateProducerForm(request.POST)

            if form.is_valid():

                # Updating the producer based on form input, only for newly inputed fields
                    post_data={}
                    if form.cleaned_data['username']:
                        username = form.cleaned_data['username']
                        post_data['username'] = username
                        #response_data['username'] = username
                    if form.cleaned_data['password']:
                        password = form.cleaned_data['password']
                        #password = make_password(password, salt=None, hasher='default')
                        post_data['password'] = password
                        #response_data['password'] = password
                    if form.cleaned_data['first_name']:
                        first_name = form.cleaned_data['first_name']
                        post_data['first_name'] = first_name
                        #response_data['first_name'] = first_name
                    if form.cleaned_data['last_name']:
                        last_name = form.cleaned_data['last_name']
                        post_data['last_name'] = last_name
                        #response_data['last_name'] = last_name
                    if form.cleaned_data['phone']:
                        phone = form.cleaned_data['phone']
                        post_data['phone'] = phone
                        #response_data['phone'] = phone
                    if form.cleaned_data['email']:
                        email = form.cleaned_data['email']
                        post_data['email'] = email
                        #response_data['email'] = email
                    if form.cleaned_data['bio']:
                        bio = form.cleaned_data['bio']
                        post_data['bio'] = bio
                        #response_data['bio'] = bio
                    if form.cleaned_data['skills']:
                        skills = form.cleaned_data['skills']
                        post_data['skills'] = skills
                        #response_data['skills'] = skills

                    #post_data['pk'] = producer_pk
                    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                    # To do: implement django form and post in exp layer
                    req = urllib.request.Request('http://exp-api:8000/api/v1/updateProducer/'+ str(producer_pk), data=post_encoded,method='POST')
                    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                    resp = json.loads(resp_json)

                    if resp['ok']:
                        response = HttpResponseRedirect(reverse('web_producer_detail', kwargs={'producer_pk': producer_pk}))
                        messages.success(request, "You successfully updated your producer account.")
                        return response
                    else:
                        response['msg'] = "Fail to update producer profile."

            else:
                #response['ok'] = False
                response['msg'] = "Invalid data sent to form."

            response['result'] = response_data
            return JsonResponse(response)

        # The form without producer's data filled in
        else:
            form = UpdateProducerForm() # need create another form?
            return render(request, 'update_producer.html', {'form': form, 'update': True, 'logged_in':logged_in, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username})

    except:
        #response['ok'] = False
        response['msg'] = "Error with updating producer."

 else:
    response['msg'] = "Unidentified user. Please log in first."

 response['result'] = response_data
 return JsonResponse(response)





@csrf_exempt
def searchConsumerResults(request):
    logged_in = True
    auth = request.COOKIES.get('auth')
    if not auth:
        logged_in = False
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    try:
      if request.method =='POST':
            form = SearchConsumerForm(request.POST)

            if form.is_valid():
                query = form.cleaned_data['query']

                post_data = {'query': query}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/searchConsumer')
                req = urllib.request.Request('http://exp-api:8000/api/v1/searchConsumer', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                #resp['ok'] = True

                if resp['ok']:
                    results = resp['result']

                    #results = [{'username': 'Xiaoying', 'password': '123@', 'first_name': 'Xiaoying', 'last_name':'Li', 'phone':'434222','email':'xxx','pk':1}]
                    return render(request, 'searchConsumer_results.html', {'form': form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in': logged_in, 'query': query, 'results': results})

                else:
                    response = HttpResponseRedirect(reverse('web_search_consumer_results'))
                    #messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_producer'))
                messages.error(request, "Invalid data sent to form in frontend.")
                return response
      else:
            form = SearchForm()
            return render(request, 'searchConsumer_results.html', {'form':form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in':logged_in, 'query': '', 'results': None})
    except:
        response = HttpResponseRedirect(reverse('web_search_consumer_results'))
        messages.error(request, "Error with search.")
        return response


@csrf_exempt
def searchProducerResults(request):
    logged_in = True
    auth = request.COOKIES.get('auth')
    if not auth:
        logged_in = False
    user_id = request.COOKIES.get('user_id')
    is_consumer = (request.COOKIES.get('is_consumer') == "True")
    username = request.COOKIES.get('username')
    try:
        if request.method =='POST':
            form = SearchProducerForm(request.POST)

            if form.is_valid():

                #response['ok'] = True

                query = form.cleaned_data['query']

                post_data = {'query': query}
                post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

                # To do: implement django form and post in exp layer
                #req = urllib.request.Request('http://exp-api:8000/api/v1/search')
                req = urllib.request.Request('http://exp-api:8000/api/v1/searchProducer', data=post_encoded,method='POST')
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
                resp = json.loads(resp_json)

                if resp['ok']:
                    #pk = resp['result']['pk']
                    results = resp['result']
                    #results = [{'title': 'Help with docker', 'description': 'Looking for someone with experience', 'consumer_username': 'mylee3', 'consumer_pk': 1, 'timestamp': 'April 2, 2018', 'pk':1}]
                    return render(request, 'searchProducer_results.html', {'form': form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in': logged_in, 'query': query, 'results': results})

                else:
                    response = HttpResponseRedirect(reverse('web_search_producer_results'))
                    #messages.error(request, resp['msg'])
                    return response
            else:
                response = HttpResponseRedirect(reverse('web_create_producer')) #??
                messages.error(request, "Invalid data sent to form in frontend.")
                return response
        else:
            form = SearchForm()
            return render(request, 'searchProducer_results.html', {'form':form, 'is_consumer':is_consumer, 'user_id':user_id, 'username': username, 'logged_in':logged_in, 'query': '', 'results': None})
    except:
        response = HttpResponseRedirect(reverse('web_search_producer_results'))
        messages.error(request, "Error with search.")
        return response
