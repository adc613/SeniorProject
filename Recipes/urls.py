from django.conf.urls import url

import views

urlpatterns = [
    url(r'creataction/(?P<recipe_pk>\d+)/$', views.CreateActionView.as_view(),
        name='create_action'),
    url(r'createrecipe/$', views.CreateRecipeView.as_view(),
        name="create_recipe")
]
