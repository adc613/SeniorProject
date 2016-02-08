from django.conf.urls import url

import views

urlpatterns = [
    url('^$', views.DevPageView.as_view(), name="dev"),
    url('^response/$', views.ResponseView.as_view(), name="response"),
]
