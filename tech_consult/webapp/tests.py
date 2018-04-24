from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
import json
from webapp.models import Consumer, Producer, Review, ConsumerRequest, Authenticator
from django.contrib.auth.hashers import make_password, check_password

#Create your tests here.
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

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class CreatedTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):
        pass  # nothing to set up

    def test_create_consumer(self):
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

    def test_create_consumer_with_duplicate_username(self):
        post_data = {'username': 'mylee3', 'password': 'password', 'first_name': 'Marissa', 'last_name': 'Lee', 'email': 'm@gmail.com', 'phone': '111-111-1111'}

        # creates the consumer
        response = self.client.post(reverse('create_consumer'), post_data)

        # checks that response contains value with same pk as created
        self.assertFalse(response.json()['ok'])


    def test_create_producer(self):
        post_data = {'username': 'megan', 'password': 'supersecret', 'first_name': 'Megan', 'last_name': 'Smith', 'email': 'msmith@hotmail.com', 'phone': '753-123-1254', 'bio': 'I am a senior at GMU.', 'skills': 'web design'}

        response = self.client.post(reverse('create_producer'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created producer
        response = self.client.get(reverse('get_producer', kwargs={'producer_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_create_producer_with_duplicate_username(self):
        post_data = {'username': 'shardi3', 'password': 'supersecret', 'first_name': 'Megan', 'last_name': 'Smith', 'email': 'msmith@hotmail.com', 'phone': '753-123-1254', 'bio': 'I am a senior at GMU.', 'skills': 'web design'}

        response = self.client.post(reverse('create_producer'), post_data)

        # checks that response contains value with same pk as created
        self.assertFalse(response.json()['ok'])

    def test_create_review(self):
        post_data = {'producer': 1, 'author': 3, 'rating': 4, 'comment': 'mylee3 got the job done well enough.'}

        response = self.client.post(reverse('create_review'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created review
        response = self.client.get(reverse('get_review', kwargs={'review_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_create_consumer_request_with_producer(self):
        post_data = {'title': 'New to Django', 'offered_price': 100, 'description': 'Django confuses me.  Can somebody teach me?', 'timestamp': 'March 6, 2018.  8:32', 'availability':'Mondays', 'consumer': 4, 'accepted_producer': 1}

        response = self.client.post(reverse('create_consumerRequest'), post_data)

        created_pk = response.json()['result']['pk']
        #print(created_pk)

        # gets the created consumer request
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': created_pk}))
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result']['pk'], created_pk)

    def test_create_consumer_request_without_producer(self):
        post_data = {'title': 'New to Django', 'offered_price': 100, 'description': 'Django confuses me.  Can somebody teach me?', 'availability':'Mondays', 'consumer': 4}

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

class DeleteTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):
        pass  # nothing to set up

    def test_delete_existing_consumer(self):
        deleted_pk = 4

        # deletes an existing consumer
        response = self.client.get(reverse('delete_consumer', kwargs={'consumer_pk': deleted_pk}))
        #print(response.json()['result'])

        # checks that response does not contain data for deleted consumer
        response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': deleted_pk}))

        self.assertFalse(response.json()['ok'])

    def test_delete_nonexisting_consumer(self):
        deleted_pk = 100

        # attempts to delete a nonexisting consumer
        response = self.client.get(reverse('delete_consumer', kwargs={'consumer_pk': deleted_pk}))
        #print(response.json()['result'])

        self.assertFalse(response.json()['ok'])

    def test_delete_existing_producer(self):
        deleted_pk = 2

        # deletes an existing consumer
        response = self.client.get(reverse('delete_producer', kwargs={'producer_pk': deleted_pk}))
        #print(response.json()['result'])

        # checks that response does not contain data for deleted producer
        response = self.client.get(reverse('get_producer', kwargs={'producer_pk': deleted_pk}))

        self.assertFalse(response.json()['ok'])

    def test_delete_nonexisting_producer(self):
        deleted_pk = 100

        # attempts to delete a nonexisting producer
        response = self.client.get(reverse('delete_producer', kwargs={'producer_pk': deleted_pk}))
        #print(response.json()['result'])

        self.assertFalse(response.json()['ok'])

    def test_delete_existing_review(self):
        deleted_pk = 1

        # deletes an existing review
        response = self.client.get(reverse('delete_review', kwargs={'review_pk': deleted_pk}))
        #print(response.json()['result'])

        # checks that response does not contain data for deleted review
        response = self.client.get(reverse('get_review', kwargs={'review_pk': deleted_pk}))

        self.assertFalse(response.json()['ok'])

    def test_delete_nonexisting_review(self):
        deleted_pk = 100

        # attempts to delete a nonexisting review
        response = self.client.get(reverse('delete_review', kwargs={'review_pk': deleted_pk}))
        #print(response.json()['result'])

        self.assertFalse(response.json()['ok'])

    def test_delete_existing_consumer_request(self):
        deleted_pk = 1

        # deletes an existing consumer request
        response = self.client.get(reverse('delete_consumerRequest', kwargs={'consumerRequest_pk': deleted_pk}))
        #print(response.json()['result'])

        # checks that response does not contain data for deleted consumer request
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': deleted_pk}))

        self.assertFalse(response.json()['ok'])

    def test_delete_nonexisting_consumer_request(self):
        deleted_pk = 100

        # attempts to delete a nonexisting consumer request
        response = self.client.get(reverse('delete_consumerRequest', kwargs={'consumerRequest_pk': deleted_pk}))
        #print(response.json()['result'])

        self.assertFalse(response.json()['ok'])

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class UpdateTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):

        pass  # nothing to set up

    def test_update_consumer_all_fields(self):

        pk=3

        post_data = {'username': 'marissa', 'password': 'password', 'first_name': 'Marissa', 'last_name': 'Lee',
                     'email': 'm@gmail.com', 'phone': '111-111-1111'}

        #response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': pk}))
        #print(response.json()['result'])

        response = self.client.post(reverse('update_consumer', kwargs={'consumer_pk': pk}), post_data)

        #print(response.json()['result'])

        #Adding pk to the post_data
        original_data = post_data
        original_data['pk'] = pk
        #print(original_data)

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']
        original_data['password'] = response.json()['result']['password']
        self.assertEquals(original_data, results)

    def test_update_consumer_one_field(self):
        pk = 3

        email = "kellym@gmail.com"

        post_data = {'email': email}

        # Getting the data before the update for comparison
        response = self.client.get(reverse('get_consumer', kwargs={'consumer_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk and updated email to original_data
        original_data['pk'] = pk
        original_data['email'] = email
        # print(original_data)

        response = self.client.post(reverse('update_consumer', kwargs={'consumer_pk': pk}), post_data)

        # print(response.json()['result'])

        # Checks that only the password of the updated data is affected
        results = response.json()['result']

        self.assertEquals(original_data, results)

    def test_update_producer_all_fields(self):

        pk=2

        post_data = {'username': 'megan', 'password': "supersecret", 'first_name': 'Megan', 'last_name': 'Smith',
                     'email': 'msmith@hotmail.com', 'phone': '753-123-1254', 'bio': 'I am a senior at GMU.',
                     'skills': 'web design'}

        #response = self.client.get(reverse('get_producer', kwargs={'producer_pk': pk}))
        #print(response.json()['result'])

        response = self.client.post(reverse('update_producer', kwargs={'producer_pk': pk}), post_data)

        #print(response.json()['result'])

        #Adding pk to the post_data
        original_data = post_data
        original_data['pk'] = pk
        #original_data['password'] = make_password(password, salt=None, hasher='default')
        #print(original_data)

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']
        original_data['password'] = response.json()['result']['password']
        self.assertEquals(original_data, results)

    def test_update_producer_one_field(self):
        pk = 2

        email = "eavery2@yahoo.com"

        post_data = {'email': email}

        # Getting the data before the update for comparison
        response = self.client.get(reverse('get_producer', kwargs={'producer_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk and updated password to original_data
        original_data['pk'] = pk
        original_data['email'] = email
        # print(original_data)

        response = self.client.post(reverse('update_producer', kwargs={'producer_pk': pk}), post_data)

        # print(response.json()['result'])

        # Checks that only the email of the updated data is affected
        results = response.json()['result']

        self.assertEquals(original_data, results)

    def test_update_review_all_fields(self):

        pk=1

        post_data = {'producer': 1, 'author': 3, 'rating': 4, 'comment': 'mylee3 got the job done well enough.'}

        #response = self.client.get(reverse('get_review', kwargs={'review_pk': pk}))
        #print(response.json()['result'])

        response = self.client.post(reverse('update_review', kwargs={'review_pk': pk}), post_data)

        #print(response.json()['result'])

        #Adding pk to the post_data
        original_data = post_data
        original_data['pk'] = pk
        #print(original_data)

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']

        self.assertEquals(original_data, results)

    def test_update_review_all_nonforeign_fields(self):

        pk=1

        #User does not change author nor producer
        post_data = {'rating': 4, 'comment': 'mylee3 got the job done well enough.'}

        response = self.client.get(reverse('get_review', kwargs={'review_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk, rating, and comment to original_data
        original_data['pk'] = pk
        original_data['rating'] = post_data['rating']
        original_data['comment'] = post_data['comment']
        # print(original_data)

        response = self.client.post(reverse('update_review', kwargs={'review_pk': pk}), post_data)

        #print(response.json()['result'])

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']

        self.assertEquals(original_data, results)

    def test_update_review_one_field(self):
        pk = 1

        rating = 4

        post_data = {'rating': rating}

        # Getting the data before the update for comparison
        response = self.client.get(reverse('get_review', kwargs={'review_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk and updated rating to original_data
        original_data['pk'] = pk
        original_data['rating'] = rating
        # print(original_data)

        response = self.client.post(reverse('update_review', kwargs={'review_pk': pk}), post_data)

        # print(response.json()['result'])

        # Checks that only the rating of the updated data is affected
        results = response.json()['result']

        self.assertEquals(original_data, results)

    def test_update_consumer_request_all_fields(self):

        pk=1

        post_data = {'title': 'New to Django', 'offered_price': 100,
                     'description': 'Django confuses me.  Can somebody teach me?',
                     'availability': 'Mondays', 'consumer': 4, 'accepted_producer': 1}

        #response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': pk}))
        #print(response.json()['result'])

        response = self.client.post(reverse('update_consumerRequest', kwargs={'consumerRequest_pk': pk}), post_data)

        #print(response.json()['result'])

        #Adding pk to the post_data
        original_data = post_data
        original_data['pk'] = pk
        #print(original_data)

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']
        original_data['timestamp'] = response.json()['result']['timestamp']
        self.assertEquals(original_data, results)

    def test_update_consumerRequest_all_nonforeign_fields(self):

        pk=3

        #User does not change consumer nor accepted_producer
        post_data = {'title': 'New to Django', 'offered_price': 100,
                     'description': 'Django confuses me.  Can somebody teach me?',
                     'availability': 'Mondays'}

        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk, rating, and comment to original_data
        original_data['pk'] = pk
        original_data['title'] = post_data['title']
        original_data['offered_price'] = post_data['offered_price']
        original_data['description'] = post_data['description']
        original_data['availability'] = post_data['availability']
        # print(original_data)

        response = self.client.post(reverse('update_consumerRequest', kwargs={'consumerRequest_pk': pk}), post_data)

        #print(response.json()['result'])

        #Checks that the updated data is the same as the posted data
        results = response.json()['result']
        original_data['timestamp'] = response.json()['result']['timestamp']

        self.assertEquals(original_data, results)

    def test_update_consumerRequest_one_field(self):
        pk = 3

        title = "Still need help"

        post_data = {'title': title}

        # Getting the data before the update for comparison
        response = self.client.get(reverse('get_consumerRequest', kwargs={'consumerRequest_pk': pk}))
        original_data = response.json()['result']

        # Adding the pk and updated title to original_data
        original_data['pk'] = pk
        original_data['title'] = title
        # print(original_data)

        response = self.client.post(reverse('update_consumerRequest', kwargs={'consumerRequest_pk': pk}), post_data)

        # print(response.json()['result'])

        # Checks that only the rating of the updated data is affected
        results = response.json()['result']
        original_data['timestamp'] = response.json()['result']['timestamp']

        self.assertEquals(original_data, results)

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class NewestConsumerRequestTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):

        pass  # nothing to set up

    def test_newest_consumer_request(self):

        response = self.client.get(reverse('get_newestConsumerRequest'))
        #print(response.json()['result'])

        newest_pk = response.json()['result']['pk']

        all_consumer_requests = ConsumerRequest.objects.all()

        # Manually checking for newest consumer request without an accepted_producer
        consumer_request = all_consumer_requests.first()
        for cr in all_consumer_requests:
            if cr.accepted_producer is None:
                consumer_request = cr

        last_pk = consumer_request.pk

        # compares the manually checked newest request with the microservice's newest request
        self.assertEquals(newest_pk, last_pk)

class HighestPriceConsumerRequestTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['db.json']

    def setUp(self):

        pass  # nothing to set up

    def test_highest_price_consumer_request(self):

        response = self.client.get(reverse('get_highestPriceConsumerRequest'))
        # print(response.json()['result'])

        highest_price = response.json()['result']['offered_price']

        all_consumer_requests = ConsumerRequest.objects.all()

        # Manually checking for highest priced consumer request without an accepted_producer
        consumer_request = all_consumer_requests.first()
        max_price = 0
        for cr in all_consumer_requests:
            if cr.accepted_producer is None and cr.offered_price > max_price:
                max_price = cr.offered_price

        # compares the manually checked highest price with the microservice's highest price
        self.assertEquals(highest_price, max_price)

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class AuthenticatorTestCase(TestCase):
    # setUp method is called before each test in this class

    fixtures = ['authenticators.json']

    def setUp(self):

        pass  # nothing to set up

    def validate_authenticator(self):
        authenticator = "e69ce6604336c5638262c6eb0ed812802e22ebde4827e2dda30c207d28ce0ee1"
        post_data = {'authenticator': authenticator}

        response = self.client.post(reverse('validate'), post_data)

        self.assertTrue(response.json()['ok'])

    def validate_invalid_authenticator(self):
        authenticator = "e69ce6604336c5638262c6eb0ed812802e22ebde4827e2dda30c207d28ce0ee2"
        post_data = {'authenticator': authenticator}

        response = self.client.post(reverse('validate'), post_data)

        self.assertFalse(response.json()['ok'])

    def test_create_authenticator_for_consumer(self):
        post_data = {'user_id': 1, 'is_consumer': True}

        response = self.client.post(reverse('create_authenticator'), post_data)
        results=response.json()['result']
        authenticator = response.json()['result']['authenticator']

        post_data_2 = {'authenticator': authenticator}

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data_2)
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result'], results)

    def test_create_authenticator_for_invalid_consumer(self):
        post_data = {'user_id': 0, 'is_consumer': True}

        response = self.client.post(reverse('create_authenticator'), post_data)
        self.assertFalse(response.json()['ok'])

    def test_create_authenticator_for_producer(self):
        post_data = {'user_id': 2, 'is_consumer': False}

        response = self.client.post(reverse('create_authenticator'), post_data)
        results = response.json()['result']
        authenticator = response.json()['result']['authenticator']

        post_data_2 = {'authenticator': authenticator}

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data_2)
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result'], results)

    def test_create_authenticator_for_invalid_producer(self):
        post_data = {'user_id': 0, 'is_consumer': False}

        response = self.client.post(reverse('create_authenticator'), post_data)
        self.assertFalse(response.json()['ok'])

    def test_login_consumer(self):
        post_data = {'username': 'mylee3', 'password': 'ilikeseals', 'is_consumer': True}

        response = self.client.post(reverse('login'), post_data)
        results = response.json()['result']
        #print("from test login, results: " + str(results))
        authenticator = response.json()['result']['authenticator']
        #print(authenticator)
        post_data_2 = {'authenticator': authenticator}

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data_2)
        #print("from test login, results: 2" + str(response.json()['result']))

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result'], results)

    def test_login_consumer_invalid_password(self):
        post_data = {'username': 'mylee3', 'password': 'password', 'is_consumer': True}

        response = self.client.post(reverse('login'), post_data)
        self.assertFalse(response.json()['ok'])

    def test_delete_authenticator_for_consumer(self):
        post_data = {'authenticator': 'e69ce6604336c5638262c6eb0ed812802e22ebde4827e2dda30c207d28ce0ee1'}

        response = self.client.post(reverse('delete_authenticator'), post_data)
        results = response.json()['result']

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data)
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertFalse(response.json()['ok'])

    def test_login_producer(self):
        post_data = {'username': 'eavery', 'password': 'lvbears', 'is_consumer': False}

        response = self.client.post(reverse('login'), post_data)
        results = response.json()['result']
        # print("from test login, results: " + str(results))
        authenticator = response.json()['result']['authenticator']
        # print(authenticator)
        post_data_2 = {'authenticator': authenticator}

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data_2)
        # print("from test login, results: 2" + str(response.json()['result']))

        # checks that response contains value with same pk as created
        self.assertEquals(response.json()['result'], results)

    def test_check_password_of_consumer(self):
        consumer_id = 1
        password = "ilikeseals"
        consumer = Consumer.objects.get(pk=consumer_id)
        self.assertTrue(check_password(password, consumer.password))

    def test_check_password_of_producer(self):
        producer_id = 1
        password = "password0"
        producer = Producer.objects.get(pk=producer_id)
        self.assertTrue(check_password(password, producer.password))

    def test_login_producer_invalid_password(self):
        post_data = {'username': 'eavery', 'password': 'password', 'is_consumer': False}

        response = self.client.post(reverse('login'), post_data)
        self.assertFalse(response.json()['ok'])

    def test_delete_authenticator_for_producer(self):
        post_data = {'user_id': 2, 'is_consumer': False}

        response = self.client.post(reverse('create_authenticator'), post_data)
        results = response.json()['result']
        authenticator = response.json()['result']['authenticator']

        post_data_2 = {'authenticator': authenticator}

        response = self.client.post(reverse('delete_authenticator'), post_data_2)
        results = response.json()['result']

        # validate the authenticator
        response = self.client.post(reverse('validate'), post_data_2)
        # print(response.json()['result'])

        # checks that response contains value with same pk as created
        self.assertFalse(response.json()['ok'])

    def test_fail(self):
        self.assertEquals("right", "wrong")

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down