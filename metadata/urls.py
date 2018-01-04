# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

js_info_dict = {
    'packages': ('metadata',),
}

urlpatterns = patterns(
    'metadata.views',
    url(r'^$', TemplateView.as_view(template_name='metadata/metadata_list.html'), name='metadata_browse'),


    # url(r'^api/batch_permissions/?$', 'batch_permissions',
    #    name='batch_permssions'),
    # url(r'^api/batch_delete/?$', 'batch_delete', name='batch_delete'),
)