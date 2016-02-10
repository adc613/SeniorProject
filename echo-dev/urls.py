from django.conf.urls import url

import views

urlpatterns = [
    url('^$', views.DevPageView.as_view(), name="home"),
    url('^response/$', views.ResponseView.as_view(), name="response"),
]
