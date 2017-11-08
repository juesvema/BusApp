from importlib import import_module

import time
from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend, get_user, user_logged_out, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.contrib.auth import logout

from apps.routes.forms import UserForm, LoginForm
from apps.routes.models import Route, UserPreference, ArrivalTime


def index(request, template_name='routes/index.html'):
    data = get_data(request)
    if data['is_authenticated']:
        data['user_preference'] = UserPreference.objects.filter(user=data['user']).first()
        if data['user_preference']:
            route = data['user_preference'].route
            station = data['user_preference'].station
            data['arrival_times'] = ArrivalTime.objects.filter(bus__route=route, station=station, time__gte=data['time_now']).order_by('time')

    return render(request, template_name, data)


def new_user(request, template_name='users/create.html'):
    data = get_data(request)
    if request.POST:
        form = UserForm(data=request.POST or None)
        if form.is_valid():
            new_user = form.save(user=None)
            login(request, new_user)
            template_name = 'routes/index.html'
            data = get_data(request)
            return render(request, template_name, data)
    else:
        data['form'] = UserForm()
    return render(request, template_name, data)


def user_login(request, template_name='routes/index.html'):
    data = get_data(request)

    return render(request, template_name, data)


def user_profile(request, template_name='users/profile.html'):
    data = get_data(request)
    if request.POST:
        form = UserForm(data=request.POST or None)
        user = form.save(data['user'])
        login(request, user)
        data = get_data(request)

    user_preference = UserPreference.objects.filter(user=data['user']).first()
    initial = {
        'first_name': data['user'].first_name,
        'last_name': data['user'].last_name,
        'email': data['user'].email
    }
    if user_preference:
        if user_preference.route:
            initial['route'] = user_preference.route.id
        if user_preference.station:
            initial['station'] = user_preference.station.id

    data['form'] = UserForm(
        initial
    )
    return render(request, template_name, data)


def user_logout(request, template_name='routes/index.html'):
    logout(request)
    data = get_data(request)
    return render(request, template_name, data)


def get_data(request):
    data = dict()
    data['time_now'] = time.strftime("%H:%M", time.localtime(time.time()))
    data['is_authenticated'] = request.user.is_authenticated()
    if not data['is_authenticated']:
        if request.POST:
            login_form = LoginForm(data=request.POST or None)
            if login_form.is_valid() and login_form.clean():
                login_form.save(request)
                data['is_authenticated'] = request.user.is_authenticated()
            else:
                data['login_form'] = login_form
        else:
            data['login_form'] = LoginForm()

    data['user'] = get_user(request)

    if data['is_authenticated']:
        data['user_preference'] = UserPreference.objects.filter(user=data['user']).first()

    routes = Route.objects.all()
    data['routes'] = routes

    return data