from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView

import sys
quant_path = '/Users/luwenjie/git/web3/quant/quant/trade_sys/quant/src/'
# quant_path = '/Users/ziyanguo/Mycode/quant/trade_sys/quant/src/'
sys.path.append(quant_path)

import parsePkl

# Create your views here.
def pattern(request):
    patternDict = parsePkl.loadPattern(quant_path + "pkl/pattern/pattern.dict")
    rsp = patternDict
    return JsonResponse(rsp)

def analyse(request):
    analyseDict = parsePkl.loadAnalyse(quant_path + "pkl/analyse/analyse.dict")
    rsp = analyseDict
    return JsonResponse(rsp)

def analyseMACD(request):
    l = parsePkl.loadMACD(quant_path + "pkl/pattern/macd.lst")
    rsp = { "rsp": l }
    return JsonResponse(rsp)

def weekends(request):
    l = parsePkl.filterWeekendsCrypto(quant_path)
    rsp = { "rsp": l }
    return JsonResponse(rsp)

def HT(request):
    l = parsePkl.loadHT(quant_path + "pkl/pattern/HT.lst")
    rsp = { "rsp": l }
    return JsonResponse(rsp)

def days(request):
    l = parsePkl.getDaysKLine(quant_path)
    rsp = { "rsp": l }
    return JsonResponse(rsp)

def fourhours(request):
    pid = request.GET.get('pid', -1)
    l = parsePkl.get4Hours(quant_path, int(pid))
    rsp = { "rsp": l }
    return JsonResponse(rsp)


def test(request):
    l = parsePkl.loadTest(quant_path + "pkl/analyse/test.lst")
    rsp = { "rsp": l }
    return JsonResponse(rsp)





