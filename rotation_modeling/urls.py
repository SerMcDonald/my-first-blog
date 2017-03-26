from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.model_main, name='model_main'),
    url(r'^build_model$', views.build_model, name='build_model'),
    url(r'^saved_models$', views.saved_models, name='saved_models'),
    url(r'^save_model$', views.save_model, name='save_model'),
    url(r'^saved_model_detail/(?P<pk>[0-9]+)$', views.saved_model_detail, name='saved_model_detail'),
   # url(r'^/build_model$', views.build_model, name='build_model'),
]