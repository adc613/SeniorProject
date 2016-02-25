from django.conf.urls import url

import views

urlpatterns = [
    url(r'^createaccount/$', views.CreateAccountView.as_view(),
        name='create_account'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^createaccount/$', views.logout, name='create_account'),

    url(r'^itworkd/$', views.ItWorkedView.as_view(), name='it_worked'),
]
