from django.conf.urls import url

import views

urlpatterns = [
    url(r'^response/$', views.ResponseView.as_view(),
        name='echo_request'),
    url(r'^selectapp/$', views.LoadApplicationView.as_view(),
        name='load_app'),
    url(r'^selectapp/(?P<pk>\d+)/$', views.ApplicationIsLoadedView.as_view(),
        name='load_app'),
]
