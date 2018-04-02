"""tech_consult_web URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from webapp_web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^request_detail/(?P<consumerRequest_pk>[0-9]+)$', views.request_detail, name='web_request_detail'),
    url(r'^consumer_detail/(?P<consumer_pk>[0-9]+)$', views.consumer_detail, name='web_consumer_detail'),
    url(r'^producer_detail/(?P<producer_pk>[0-9]+)$', views.producer_detail, name='web_producer_detail'),
    url(r'^login$',views.login, name='web_login'),
    url(r'^logout$',views.logout),
    url(r'^create_listing$',views.createListing, name='web_create_listing'),
    url(r'^create_consumer$',views.createConsumer, name='web_create_consumer'),
    url(r'^create_producer$',views.createProducer, name='web_create_producer'),
    url(r'^search_results$',views.searchResults, name='web_search_results'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
