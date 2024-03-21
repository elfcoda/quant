#!/usr/bin/env python
# encoding: utf-8

from django.urls import path

from . import views
app_name = 'trade_sys'

urlpatterns = [
    path("pattern/", views.pattern, name='pattern'),
    path("analyse/", views.analyse, name='analyse'),
    path("analyseMACD/", views.analyseMACD, name='analyseMACD'),
    path("weekends/", views.weekends, name='weekends'),
    path("HT/", views.HT, name='HT'),
    path("test/", views.test, name='test'),
    path("days/", views.days, name='days'),
    path("fourhours/", views.fourhours, name='fourhours'),
]
