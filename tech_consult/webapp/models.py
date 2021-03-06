from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Consumer(models.Model):
    username = models.CharField(max_length=200, default="none", unique=True)
    password = models.CharField(max_length=500, default="none")
    first_name = models.CharField(max_length=200, default="none")
    last_name = models.CharField(max_length=200, default="none")
    phone = models.CharField(max_length=200, default="none")
    email = models.EmailField(max_length=200, default="none")
    #user = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.username)

class Producer(models.Model):
    username = models.CharField(max_length=200, default="none", unique=True)
    password = models.CharField(max_length=500, default="none")
    first_name = models.CharField(max_length=200, default="none")
    last_name = models.CharField(max_length=200, default="none")
    phone = models.CharField(max_length=200, default="none")
    email = models.EmailField(max_length=200, default="none")
    bio = models.CharField(max_length=250, default="none")
    skills = models.CharField(max_length=200, default="none")
   

    def __str__(self):
        return "%s" % (self.username)

class Review(models.Model):
    rating = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="none")
    producer = models.ForeignKey(Producer, default=1)
    author = models.ForeignKey(Consumer, default=1)

# def __str__(self):
#      return "%s" % (self.username)

class ConsumerRequest(models.Model):
    title = models.CharField(max_length=50, default="none")
    offered_price = models.FloatField(max_length=10)
    description = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=50)
    availability = models.CharField(max_length=50)
    consumer = models.ForeignKey(Consumer, default=1)
    accepted_producer = models.ForeignKey(Producer, null=True)

#  def __str__(self):
#       return self.description

class Authenticator(models.Model):
    authenticator = models.CharField(max_length=255, primary_key=True)
    #Using user_id and is_consumer for Consumer and Producer models
    user_id = models.IntegerField(default=0)
    is_consumer = models.BooleanField(default=True)
    date_created = models.CharField(max_length=50)

class Recommendation(models.Model):
    item_id = models.ForeignKey(ConsumerRequest, default=1)
    recommended_items = models.CharField(max_length=100)