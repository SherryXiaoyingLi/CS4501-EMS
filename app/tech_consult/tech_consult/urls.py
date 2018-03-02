"""tech_consult URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from webapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/consumers/create$', views.create_consumer, name='create_consumer'),
    url(r'^api/v1/consumers/(?P<consumer_pk>[0-9]+)$', views.get_consumer, name='get_consumer'),
    url(r'^api/v1/consumers/(?P<consumer_pk>[0-9]+)/update$', views.update_consumer, name='update_consumer'),
    url(r'^api/v1/consumers/(?P<consumer_pk>[0-9]+)/delete$', views.delete_consumer, name='delete_consumer'),
    url(r'^api/v1/producers/create$', views.create_producer, name='create_producer'),
    url(r'^api/v1/producers/(?P<producer_pk>[0-9]+)$', views.get_producer, name='get_producer'),
    url(r'^api/v1/producers/(?P<producer_pk>[0-9]+)/update$', views.update_producer, name='update_producer'),
    url(r'^api/v1/producers/(?P<producer_pk>[0-9]+)/delete$', views.delete_producer, name='delete_producer'),
    url(r'^api/v1/reviews/create$', views.create_review, name='create_review'),
    url(r'^api/v1/reviews/(?P<review_pk>[0-9]+)$', views.get_review, name='get_review'),
    url(r'^api/v1/reviews/(?P<review_pk>[0-9]+)/update$', views.update_review, name='update_review'),
    url(r'^api/v1/reviews/(?P<review_pk>[0-9]+)/delete$', views.delete_review, name='delete_review'),
    url(r'^api/v1/consumerRequests/create$', views.create_consumerRequest, name='create_consumerRequest'),
    url(r'^api/v1/consumerRequests/(?P<consumerRequest_pk>[0-9]+)$', views.get_consumerRequest, name='get_consumerRequest'),
    url(r'^api/v1/consumerRequests/(?P<consumerRequest_pk>[0-9]+)/update$', views.update_consumerRequest, name='update_consumerRequest'),
    url(r'^api/v1/consumerRequests/(?P<consumerRequest_pk>[0-9]+)/delete$', views.delete_consumerRequest, name='delete_consumerRequest'),
    url(r'^api/v1/consumerRequests/getHighestPrice$', views.getHighestPriceConsumerRequest, name='get_highestPriceConsumerRequest'),
    url(r'^api/v1/consumerRequests/getNewest$', views.getNewestConsumerRequest, name='get_newestConsumerRequest'),
]
