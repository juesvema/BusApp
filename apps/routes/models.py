# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Route(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    origin = models.CharField(_('Orígen'), max_length=255, blank=True, null=True)
    destination = models.CharField(_('Destino'), max_length=255, blank=True, null=True)
    url = models.TextField(_('Dirección'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = "Rutas"


class Station(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    route = models.ForeignKey(Route, verbose_name=_('Ruta'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estación'
        verbose_name_plural = "Estaciones"


class Bus(models.Model):
    code = models.CharField(_('Código del bus'), max_length=255)
    route = models.ForeignKey(Route, verbose_name=_('Ruta'), blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = "Buses"


class ArrivalTime(models.Model):
    bus = models.ForeignKey(Bus, verbose_name=_('Bus'), blank=True, null=True)
    station = models.ForeignKey(Station, verbose_name=_('Estación'), blank=True, null=True)
    time = models.TimeField(_('Hora de llegada'), null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.time)

    class Meta:
        verbose_name = 'Tiempo de llegada'
        verbose_name_plural = "Tiempos de llegada"


class UserPreference(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Usuario'))
    route = models.ForeignKey(Route, verbose_name=_('Ruta'), blank=True, null=True)
    arrival_time = models.ForeignKey(ArrivalTime, verbose_name=_('Tiempo de llegada'), blank=True, null=True)
    station = models.ForeignKey(Station, verbose_name=_('Estación actual de usuario'), blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.id)

    class Meta:
        verbose_name = 'Preferencia de usuario'
        verbose_name_plural = "Preferencias de usuario"