from django.conf.urls import url

import views

urlpatterns = [
    url(r'^createaccount/$', views.ResponseView.as_view(),
        name='echo_request'),
]
