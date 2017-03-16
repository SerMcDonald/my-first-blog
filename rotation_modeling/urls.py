from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.model_main, name='model_main'),
    url(r'^build_model$', views.build_model, name='build_model'),
   # url(r'^/build_model$', views.build_model, name='build_model'),
]