from django.http import HttpResponse
from django.http import HttpRequest
import json
from atlas.services import clustering_service


def getReviewClusteringData(request):
    kw = request.GET['query']
    engine = request.GET['engine']
    print kw
    if "." in kw:
        kw = str(kw).split(".")[0]
    return HttpResponse((clustering_service.getRevClusteringData(kw, engine)), status=200)


def getSocialClusteringData(request):
    kw = request.GET['query']
    engine = request.GET['engine']
    print kw
    if "." in kw:
        kw = str(kw).split(".")[0]
    return HttpResponse((clustering_service.getSocClusteringData(kw, engine)), status=200)


def getUploadClusteringData(request):
    kw = request.GET['query']
    engine = request.GET['engine']
    print kw
    if "." in kw:
        kw = str(kw).split(".")[0]
    return HttpResponse((clustering_service.getUplClusteringData(kw, engine)), status=200)


def getFullImport(request):
    return HttpResponse((clustering_service.getFullImport()), status=200)