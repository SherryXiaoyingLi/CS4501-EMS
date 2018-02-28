from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
import json
from webapp.models import Consumer, Producer, Review, ConsumerRequest

# Create your tests here.
class GetConsumerTestCase(TestCase):
    # setUp method is called before each test in this class

    #fixtures = ['db.json']

    def setUp(self):
        pass  # nothing to set up

    def test_get_created_consumer(self):
        post_data = {'username': 'mylee3', 'password': 'password', 'first_name': 'Marissa', 'last_name': 'Lee', 'email': 'm@gmail.com', 'phone': '111-111-1111'}

        response = self.client.post(reverse('create_consumer'), post_data)
        #self.client.post('/api/v1/consumers/create')
        #resp = json.loads(resp_json)
        #print(resp)

        # assumes consumer with id 1 is stored in db
        response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': 1}))
        print(response.json()['result'])
        print(response.json()['ok'])
        # checks that response contains parameter order list & implicitly
        # checks that the HTTP status code is 200
        self.assertContains(response, 'result')

    # user_id not given in url, so error
    #def fails_invalid(self):
    #    response = self.client.get(reverse('all_orders_list'))
    #    self.assertEquals(response.status_code, 404)

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down