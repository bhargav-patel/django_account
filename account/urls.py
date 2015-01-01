from django.conf.urls import patterns, include, url
from views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', account_view,name='account'),
	url(r'^login/$', login_view,name='login'),
	url(r'^logout/$', logout_view,name='logout'),
	url(r'^register/$', register_view,name='register'),
	url(r'^password_change/$', password_change_view,name='password_change'),
	url(r'^activate/(?P<activation_key>\w+)/$', activate_view),
	url(r'^reset/$', reset_view,name='reset'),
	url(r'^reset/(?P<activation_key>\w+)/$', reset_activate_view,name='reset_activate'),
)
