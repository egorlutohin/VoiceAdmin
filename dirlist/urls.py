from django.conf.urls import patterns, url
from dirlist import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<phone_number>[0-9A-Za-z_]+)/$', views.dates_index, name="dates_index"),
    url(r'^(?P<phone_number>[0-9A-Za-z_]+)/(?P<date_dir>[0-9-]+)/$', views.records_index, name="records_index"),
    url(r'^(?P<phone_number>[0-9A-Za-z_]+)/(?P<date_dir>[0-9-]+)/(?P<record_file>[^/]+)$', views.deliver_record, name="deliver_record"),
)
