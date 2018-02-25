"""VoiceAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, patterns
from django.conf import settings

urlpatterns = [
    url(r'', include('dirlist.urls', namespace='dirlist')),
	url(r'^%s$' % settings.LOGIN_URL[1:], 'django.contrib.auth.views.login', name='login'),
    url(r'^%s$' % settings.LOGOUT_URL[1:], 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}, name='logout',),    
]

if settings.DEBUG:
    from django.views.generic import TemplateView
    urlpatterns += patterns('',
        (r'^static\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS, 'show_indexes': True}),
        (r'^403.html$', TemplateView.as_view(template_name="403.html")),
        (r'^404.html$', TemplateView.as_view(template_name="404.html")),
        (r'^500.html$', TemplateView.as_view(template_name="500.html")),
    )
