#!/usr/bin/env python
# encoding: utf-8

from django.urls import path

from . import views
app_name = 'trade_sys'

urlpatterns = [
    path("test/", views.test, name='test'),
    path("analyse/", views.analyse, name='analyse'),
]
