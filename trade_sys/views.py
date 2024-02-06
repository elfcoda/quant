from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView

import sys
quant_path = '/Users/luwenjie/git/web3/quant/quant/trade_sys/quant/src/'
sys.path.append(quant_path)

import parsePkl

# Create your views here.
def test(request):
    patternDict = parsePkl.loadPattern(quant_path + "pkl/pattern/pattern.dict")
    rsp = patternDict
    return JsonResponse(rsp)

def analyse(request):
    analyseDict = parsePkl.loadAnalyse(quant_path + "pkl/analyse/analyse.dict")
    rsp = analyseDict
    return JsonResponse(rsp)

