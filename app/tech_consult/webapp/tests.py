from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
import json
from webapp.models import Consumer, Producer, Review, ConsumerRequest



class GetTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):

        pass  # nothing to set up

    def test_get_consumer_from_fixture(self):

        pk=1

        # assumes consumer with id 1 is stored in db after loading fixtures
        response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': pk}))
        #print(response.json()['result'])

        # checks that response contains value insude the result
        self.assertEquals(response.json()['result']['pk'], pk)

    # producer pk not given in url, so error
    def invalid_consumer_no_pk(self):
        response = self.client.get(reverse('get_consumer'))

        #print(response.json()['ok'])
        self.assertFalse(response.json()['ok'])

    def test_get_producer_from_fixture(self):

        pk=1

        # assumes producer with id 1 is stored in db after loading fixtures
        response = self.client.get(reverse('get_producer', kwargs={'producer_pk': pk}))
        #print(response.json()['result'])

        # checks that response contains value insude the result
        self.assertEquals(response.json()['result']['pk'], pk)

    # producer pk not given in url, so error
    def invalid_producer_no_pk(self):
        response = self.client.get(reverse('get_producer'))

        #print(response.json()['ok'])
        self.assertFalse(response.json()['ok'])

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

    def test_get_review_from_fixture(self):

        pk=1

        # assumes review with id 1 is stored in db after loading fixtures
        response = self.client.get(reverse('get_review', kwargs={'review_pk': pk}))
        #print(response.json()['result'])

        # checks that response contains value insude the result
        self.assertEquals(response.json()['result']['pk'], pk)

    # review id not given in url, so error
    def invalid_review_no_pk(self):
        response = self.client.get(reverse('get_review'))

        #print(response.json()['ok'])
        self.assertFalse(response.json()['ok'])

    def test_get_consumer_request_from_fixture(self):

        pk=1

        # assumes consumer request with id 1 is stored in db after loading fixtures
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': pk}))
        #print(response.json()['result'])

        # checks that response contains value insude the result
        self.assertEquals(response.json()['result']['pk'], pk)

    # consumer request pk not given in url, so error
    def invalid_consumer_request_no_pk(self):
        response = self.client.get(reverse('get_consumerRequest'))

        #print(response.json()['ok'])
        self.assertFalse(response.json()['ok'])

#Create your tests here.
class GetCreatedTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):
        pass  # nothing to set up

    def test_get_created_consumer(self):
        post_data = {'username': 'marissa', 'password': 'password', 'first_name': 'Marissa', 'last_name': 'Lee', 'email': 'm@gmail.com', 'phone': '111-111-1111'}

        # creates the consumer
        response = self.client.post(reverse('create_consumer'), post_data)
        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created consumer
        response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': created_pk}))
        #print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_get_created_producer(self):
        post_data = {'username': 'megan', 'password': 'supersecret', 'first_name': 'Megan', 'last_name': 'Smith', 'email': 'msmith@hotmail.com', 'phone': '753-123-1254', 'bio': 'I am a senior at GMU.', 'skills': 'web design'}

        response = self.client.post(reverse('create_producer'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created producer
        response = self.client.get(reverse('get_producer', kwargs={'producer_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_get_created_review(self):
        post_data = {'producer': 1, 'author': '3', 'rating': 4, 'comment': 'mylee3 got the job done well enough.'}

        response = self.client.post(reverse('create_review'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created review
        response = self.client.get(reverse('get_review', kwargs={'review_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_get_created_consumer_request_with_producer(self):
        post_data = {'title': 'New to Django', 'offered_price': 100, 'description': 'Django confuses me.  Can somebody teach me?', 'timestamp': 'March 6, 2018.  8:32', 'availability':'Mondays', 'consumer': 4, 'accepted_producer': 1}

        response = self.client.post(reverse('create_consumerRequest'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created consumer request
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_get_created_consumer_request_without_producer(self):
        post_data = {'title': 'New to Django', 'offered_price': 100, 'description': 'Django confuses me.  Can somebody teach me?', 'timestamp': 'March 6, 2018.  8:32', 'availability':'Mondays', 'consumer': 4}

        response = self.client.post(reverse('create_consumerRequest'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created consumer request
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': created_pk}))
        #print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down