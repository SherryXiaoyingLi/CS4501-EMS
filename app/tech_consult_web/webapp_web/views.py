from django.shortcuts import render
from django.shortcuts import render_to_response

import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse

def index(request):
    context_dict = {'newest_pk': 1, 'highest_pk': 1}

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

        return render(request, "request_detail.html", context_dict)

    else:
        return HttpResponse("Consumer request does not exist.")


#for login page
#read login info, pass to log in exp srvc, receive authenticator back if password correct
#if successfully logged in, pass in cookie to browser
#if failed, return login failure response
def login (request):
    #need to add login form here???
    resultResp= {}
    response= {}
    
    req = urllib.request.Request('http://exp-api:8000/api/v1/login/') #change url???  data readin???
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
                
    if resp['ok']:
        
         resultResp['authenticator'] = resp['result']['authenticator']
         cookie_key =resultResp['authenticator']['user_id']
         cookie_value = resultResp['authenticator']
         response = render(request, "login.html")
            
         #set cookie and use user_id as cookie key/name/id
         response.set_cookie(key=cookie_key,value=cookie_value,path='/',domain=None)
         return response
    
    else:
         return HttpResponse("Log in validation failed. Please create account first.")


#for logout page
#remove the HTTP cookie and call delete
#def logout(request):



