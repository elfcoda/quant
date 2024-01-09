from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

# Create your views here.
def test(request):
    return HttpResponse("You're looking at question.")

