# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from apps.routes.models import Route, UserPreference, Station


class UserForm(forms.Form):
    first_name = forms.CharField(label=_('Nombre'),max_length=100,
                           widget=forms.TextInput(attrs={
                               'required':'',
                                'class':'validate',
                           }))
    last_name = forms.CharField(label=_('Apellido'), max_length=100,
                           widget=forms.TextInput(attrs={
                               'required': '',
                               'class': 'validate',
                           }))
    email = forms.CharField(label=_('Email'),max_length=100,
                           widget=forms.EmailInput(attrs={
                               'required':'',
                               'class': 'validate',
                           }))
    password1 = forms.CharField(label=_('Contraseña'), max_length=100, required=False,
                                widget=forms.PasswordInput(
                                attrs={
                                    'required': '',
                                    'class': 'validate',
                                }))
    password2 = forms.CharField(label=_('Confirmar contraseña'), max_length=100, required=False,
                                widget=forms.PasswordInput(
                                attrs={
                                    'required': '',
                                    'class': 'validate',
                                }))
    route = forms.ModelChoiceField(label=_('Ruta preferida'), queryset=Route.objects.all(), required=False,
                                             widget=forms.Select(attrs={
                                                 'class': 'validate',
                                             }))
    station = forms.ModelChoiceField(label=_('Estación actual'), queryset=Station.objects.all(),
                                     required=False,
                                     widget=forms.Select(attrs={
                                         'class': 'validate',
                                     }))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password1')
        password_confirm = cleaned_data.get('password2')
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password1', 'La contraseña y la confirmación no coinciden')

        return cleaned_data

    def save(self, user):
        if user:
            user.first_name = self.data['first_name']
            user.last_name = self.data['last_name']
            user.email = self.data['email']
            route = self.data['route']
            station = self.data['station']
            user_preference = UserPreference.objects.filter(user__pk=user.id).first()
            if not user_preference:
                user_preference = UserPreference(
                    user=user,
                )
            if route:
                object_route = Route.objects.filter(pk=route).first()
                user_preference.route = object_route
            else:
                user_preference.route = None
            if station:
                object_station = Station.objects.filter(pk=station).first()
                user_preference.station = object_station
            else:
                user_preference.station = None
            user_preference.save()

            user.save()
        else:
            object_user = User.objects.create_user(
                username=self.cleaned_data['email'][:29],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1'],
                is_staff=False,
            )
            object_user.save()
            return object_user

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Nombre'),max_length=100,
                           widget=forms.TextInput(attrs={
                               'required':'',
                                'class':'validate',
                           }))

    password = forms.CharField(label=_('Contraseña'),min_length=6, max_length=100, required=True,
                                widget=forms.PasswordInput(
                                attrs={
                                    'required': '',
                                    'class': 'validate',
                                }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                return cleaned_data
        self.add_error('username', 'El usuario y la contraseña no coinciden')
        self.add_error('password', 'El usuario y la contraseña no coinciden')
        return cleaned_data


    def save(self,request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                login(request, user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
        return user