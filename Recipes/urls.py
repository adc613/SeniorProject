from django.conf.urls import url

import views

urlpatterns = [
    url(r'creataction/(?P<recipe_pk>\d+)/$', views.CreateActionView.as_view(),
        name='create_action'),
    url(r'createrecipe/$', views.CreateRecipeView.as_view(),
        name="create_recipe"),
    url(r'editbrt/(?P<pk>\d+)/$', views.EditBasicReturnTextView.as_view(),
        name='edit_basic_return_text'),
    url(r'addapit/(?P<pk>\d+)/$', views.AddAPICallView.as_view(),
        name='add_api_call'),
]
