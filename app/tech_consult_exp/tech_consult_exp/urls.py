"""tech_consult_exp URL Configuration

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
from webapp_exp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^api/v1/getNewestRequestPk$', views.getNewestRequestPk, name='get_newestRequestPk'),
    url(r'^api/v1/getHighestRequestPk$', views.getHighestRequestPk, name='get_highestRequestPk'),
    url(r'^api/v1/requestDetail/(?P<consumerRequest_pk>[0-9]+)$', views.getRequestDetail, name='exp_requestDetail'),
    url(r'^api/v1/consumerDetail/(?P<consumer_pk>[0-9]+)$', views.getConsumerDetail, name='exp_consumerDetail'),
    url(r'^api/v1/producerDetail/(?P<producer_pk>[0-9]+)$', views.getProducerDetail, name='exp_producerDetail'),
    url(r'^api/v1/login$', views.login, name='login'),
    url(r'^api/v1/logout$', views.logout, name='logout'),
    url(r'^api/v1/createListing$', views.createListing, name='create_listing'),
    url(r'^api/v1/createConsumer$', views.createConsumer, name='create_consumer'),
    url(r'^api/v1/createProducer$', views.createProducer, name='create_producer'),
    url(r'^api/v1/search$', views.search, name='search'),
]
