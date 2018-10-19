from django.http import HttpResponse
from django.http import HttpRequest
import json
from atlas.services import summary_service


def getCountRevCardsData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((summary_service.getCountRevCards(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getCountRevCardsOverallData(request):
    kw = request.GET['query']
    return HttpResponse(summary_service.getCountRevCardsOverall(kw), status=200)


def getTopposPostsData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    topn = request.GET['topn']
    return HttpResponse(summary_service.getTopposPosts(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate), json.loads(topn)), status=200)


def getTopnegPostsData(request):
    kw = request.GET['query']
    topn = request.GET['topn']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']

    return HttpResponse(summary_service.getTopnegPosts(kw, json.loads(brand), json.loads(source),
                                   json.loads(sku), json.loads(fromDate), json.loads(toDate), json.loads(topn)), status=200)


def getTopposOverallData(request):
    kw = request.GET['query']
    topn = request.GET['topn']
    return HttpResponse(summary_service.getTopposPostsOverall(kw, json.loads(topn)), status=200)


def getTopnegOverallData(request):
    kw = request.GET['query']
    topn = request.GET['topn']
    return HttpResponse(summary_service.getTopnegPostsOverall(kw, json.loads(topn)), status=200)


def getTopposnegData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((summary_service.getTopposneg(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getPivotdata(request):
    kw = request.GET['query']
    # if "." in kw:
    #     kw = str(kw).split(".")[0]
    return HttpResponse((summary_service.getPivotcontent(kw)), status=200)


def getAssocDims(request):
    kw = request.GET['query']
    print kw
    if "." in kw:
        kw = str(kw).split(".")[0]
    return HttpResponse((summary_service.getAssocDims(kw)), status=200)


def getAssocLevels(request):
    kw = request.GET['query']
    dim = request.GET['dim']
    print kw
    if "." in kw:
        kw = str(kw).split(".")[0]
    return HttpResponse((summary_service.getAssocLevels(kw, dim)), status=200)


def getAssociationMapdata(request):
    kw = request.GET['query']
    dim = request.GET['dim']
    print(dim)
    # lev = request.GET['lev']
    return HttpResponse((summary_service.getAssociationdata(kw, dim)), status=200)


def getTopposnegOverallData(request):
    kw = request.GET['query']
    return HttpResponse(summary_service.getTopposnegOverall(kw), status=200)


def getBrandFilter(request):
    kw = request.GET['query']
    return HttpResponse((summary_service.getBrand(kw)), status=200)


def getSourceFilter(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    # print(kw, json.loads(brand))
    return HttpResponse((summary_service.getSource(kw, json.loads(brand))), status=200)


def getSourceRevmap(source_vals):
    return HttpResponse(summary_service.getSourceRevmap1(source_vals), status=200)


def getSkuFilter(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    return HttpResponse((summary_service.getSku(kw, json.loads(brand), json.loads(source))), status=200)


def getChart1Data(request):
    kw = request.GET['query']
    print(kw)
    brand = request.GET['brand']
    print(brand)
    source = request.GET['source']
    print(source)
    sku = request.GET['sku']
    print(sku)
    fromDate = request.GET['fromDate']
    print(fromDate)
    toDate = request.GET['toDate']
    print(toDate)
    return HttpResponse((summary_service.getChart1(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getCommonReviewCountChartData(request):
    print("inside getreviewcountchartdata")
    kw = request.GET['query']
    return HttpResponse(summary_service.getCommonReviewCountChart(kw), status=200)


# def getChart2Data(request):
#     kw = request.GET['query']
#     brand = request.GET['brand']
#     source = request.GET['source']
#     sku = request.GET['sku']
#     fromDate = request.GET['fromDate']
#     toDate = request.GET['toDate']
#     return HttpResponse((summary_service.getChart2(kw, json.loads(brand), json.loads(source),
#                                               json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getChart3Data(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((summary_service.getChart3(kw, json.loads(brand), json.loads(source),
                                               json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getPieChartData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']
    return HttpResponse((summary_service.getPieChart(kw, json.loads(brand), json.loads(source),
                                               json.loads(sku), json.loads(fromDate), json.loads(toDate))), status=200)


def getCategChartRevData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']

    return HttpResponse(summary_service.getCategChartRev(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate)), status=200)


def getCategChartData(request):
    kw = request.GET['query']

    return HttpResponse(summary_service.getCategChart(kw), status=200)


def getWordCloudRevData(request):
    kw = request.GET['query']
    brand = request.GET['brand']
    source = request.GET['source']
    sku = request.GET['sku']
    fromDate = request.GET['fromDate']
    toDate = request.GET['toDate']

    return HttpResponse(summary_service.getWordCloudRev(kw, json.loads(brand), json.loads(source),
                                       json.loads(sku), json.loads(fromDate), json.loads(toDate)), status=200)


def getWordCloudData(request):
    kw = request.GET['query']

    if "." in kw:
        kw = str(kw).split(".")[0]

    return HttpResponse(summary_service.getWordCloud(kw), status=200)