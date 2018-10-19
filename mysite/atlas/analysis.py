
from django.http import HttpResponse
from django.http import HttpRequest
import json
from atlas.services import analysis_service


def getBrandFilter(request):
    kw = request.GET['query']
    return HttpResponse((analysis_service.getBrand(kw)), status=200)


def reloadBrandFilterWithSrc(request):
    # print(request)
    kw = request.GET['query']
    src = request.GET['source']
    return HttpResponse((analysis_service.reloadBrandWithSrc(kw, json.loads(src))), status=200)


def reloadBrandFilterWithSku(request):
    # print(request)
    kw = request.GET['query']
    sku = request.GET['sku']
    return HttpResponse((analysis_service.reloadBrandWithSku(kw, json.loads(sku))), status=200)


def getSourceFilter(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    # print(kw, json.loads(brand))
    return HttpResponse((analysis_service.getSource(kw, json.loads(brand))), status=200)


def reloadSourceFilterWithBrd(request):
    # print(request)
    kw = request.GET['query']
    brd = request.GET['brand']
    return HttpResponse((analysis_service.reloadSourceWithBrd(kw, json.loads(brd))), status=200)


def reloadSourceFilterWithSku(request):
    # print(request)
    kw = request.GET['query']
    sku = request.GET['sku']
    return HttpResponse((analysis_service.reloadSourceWithSku(kw, json.loads(sku))), status=200)


def getSkuFilter(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    return HttpResponse((analysis_service.getSku(kw, json.loads(brand), json.loads(source))), status=200)


def reloadSkuFilterWithBrd(request):
    # print(request)
    kw = request.GET['query']
    brand = request.GET['brand']
    return HttpResponse((analysis_service.reloadSkuWithBrd(kw, json.loads(brand))), status=200)


def reloadSkuFilterWithSrc(request):
    # print(request)
    kw = request.GET['query']
    src = request.GET['source']
    return HttpResponse((analysis_service.reloadSkuWithSrc(kw, json.loads(src))), status=200)


def getBrandSummaryChartData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((analysis_service.getBrandSummaryChart(kw, json.loads(brand), json.loads(source),
                                               json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getChart1Data(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((analysis_service.getChart1(kw, json.loads(brand), json.loads(source), json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getChart2Data(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((analysis_service.getChart2(kw, json.loads(brand), json.loads(source), json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getChart3Data(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((analysis_service.getChart3(kw, json.loads(brand), json.loads(source), json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getCommonTrigChartData(request):
    kw = request.GET['query']
    return HttpResponse(analysis_service.getCommonTrigChart(kw), status=200)


def getChart4Data(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((analysis_service.getChart4(kw, json.loads(brand), json.loads(source), json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getCommonDrivChartData(request):
    kw = request.GET['query']
    return HttpResponse(analysis_service.getCommonDrivChart(kw), status=200)


def getCommonSentiChartData(request):
    kw = request.GET['query']
    return HttpResponse(analysis_service.getCommonSentiChart(kw), status=200)
