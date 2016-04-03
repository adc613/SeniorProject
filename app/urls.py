"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from accounts.views import HomePageView, HowItWorksView, AboutUsView, IOTView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^aboutus/$', AboutUsView.as_view(), name='aboutus'),
    url(r'^howitworks/$', HowItWorksView.as_view(), name='howitworks'),
    url(r'^iot/$', IOTView.as_view(), name='iot'),
    url(r'^dev/', include('echo-dev.urls', namespace='dev')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^recipes/', include('Recipes.urls', namespace='Recipes')),
    url(r'^session/', include('session.urls', namespace='session')),

    url(r'^admin/', admin.site.urls),
]
