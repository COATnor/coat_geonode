from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
#from newdata.urls import nd_api
from rest_framework import routers, serializers, viewsets

from geonode.urls import *

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
   (r'^metadata/', include('metadata.urls')),
   (r'^newdata/', include('newdata.urls')),
   #(r'', include(nd_api.urls)),
   (r'^newdatadrf/', include('rest_framework.urls')),
 ) + urlpatterns
