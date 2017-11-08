from django.conf.urls import url, include
from django.contrib.auth import logout

from apps.routes.views import index, user_logout, new_user, user_profile

urlpatterns = [
    url(r'^logout', user_logout, name='user_logout'),
    url(r'^register', new_user, name='new_user'),
    url(r'^user_profile', user_profile, name='user_profile'),
    url(r'^', index),
]
