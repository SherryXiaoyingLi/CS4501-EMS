from django.db import models

# Create your models here.

class ConsumerRequest(models.model):
    title = models.CharField(max_length=50, default="none")
    offered_price = models.FloatField(max_length=10)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add = True)
    availability = models.CharField(max_length=50)
    consumer = models.ForeignKey(Consumer)
    accepted_producer = models.ForeignKey(Producer)

    def __str__(self):
        return self.description

class Consumer(models.model):
    username = models.CharField(max_length=200, default="none", unique=True)
	password = models.CharField(max_length=200, default="none")
	first_name = models.CharField(max_length=200, default="none")
	last_name = models.CharField(max_length=200, default="none")
	phone = models.CharField(max_length=200, default="none")
    email = models.EmailField(max_length=200, default="none")
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.username)

class Producer(models.model):
    username = models.CharField(max_length=200, default="none", unique=True)
	password = models.CharField(max_length=200, default="none")
	first_name = models.CharField(max_length=200, default="none")
	last_name = models.CharField(max_length=200, default="none")
	phone = models.CharField(max_length=200, default="none")
    email = models.EmailField(max_length=200, default="none")
    bio = models.CharField(max_length=250, default="none")
    skills = models.CharField(max_length=200, default="none")
    review = models.ForeignKey(Review)
    consumer = models.ForeignKey(Consumer)
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.username)

class Review(models.model):
    rating = models.IntegerField(default = 0)
    author = models.CharField(max_length=50, default"none")
    comment = models.CharField(max_length=150, default"none")
