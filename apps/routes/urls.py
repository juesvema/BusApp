from django.conf.urls import url, include
from apps.routes.views import index
urlpatterns = [
    url(r'^', index),
]
