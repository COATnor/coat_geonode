# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

js_info_dict = {
    'packages': ('newdata',),
}

urlpatterns = patterns(
    'newdata.views',
    url(r'^$', TemplateView.as_view(template_name='newdata/newdata_list.html'), name='newdata_browse'),
)