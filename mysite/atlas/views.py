from __future__ import absolute_import
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import HttpRequest
import json
from atlas.services import product_service
import traceback
from django.views.decorators.csrf import        ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from atlas.forms import PasswordResetForm
from atlas.forms import SignUpForm
from atlas.config import dbConfig
import pandas as pd
from django.db import connection
from django.db.models import F
#import csv
import os
from collections import OrderedDict
from atlas.models import Requests, Product, Review, Analysis, Uploads, UploadAnalyses, DimenMap, TagDicts, TagDictsUpl, Social, SocialAnalyses, TaggedData, TaggedDataUpl, TaggedDataRev, AggTaggedData, AggTaggedDataUpl, AggTaggedDataRev, ContentCategoryRev, ContentCategoryUpl, ContentCategorySoc
import re
# from django.core.serializers.json import DjangoJSONEncoder
#
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
# import six
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dbConfig.dict['gcp_servicekey_path']
sys.path.append(dbConfig.dict['spiderPath'])


@login_required(login_url="/login/")
def index(request):
    return render(request, 'atlas/index.html')


def home(request):
    return render(request, 'atlas/index.html')


def search(request):
    return render(request, 'atlas/Search.html')


def queue(request):
    return render(request, 'atlas/Queue.html')


def summary(request):
    return render(request, 'atlas/Summary.html')


def topicmodeling(request):
    print("inside view.topicmodeling")
    query = request.GET['request']
    print query
    try:
        if query.index('.csv'):
            query = str(query).split('.')[0]
            print(query)
    except:
        print(query)

    try:
        return render(request, 'atlas/Topic.html', {'product': str("atlas/includes/" + query + ".html")})
    except:
        print(traceback.print_exc())
        return render(request, 'atlas/Topic.html', {'product': str("atlas/includes/error.html")})


def clustering(request):
    print(request)
    query = request.GET['request']
    try:
        if query.index('.csv'):
            query = str(query).split('.')[0]
            print(query)
    except:
        print(query)

    try:
        return render(request, 'atlas/Clustering.html', {'product1': str("atlas/includes/" + query + ".html")})
    except:
        print(traceback.print_exc())
        return render(request, 'atlas/Clustering.html', {'product1': str("atlas/includes/error.html")})


def pivot(request):
    #query = request.GET['request']
    return render(request, 'atlas/Pivot.html')


def association(request):
    #query = request.GET['request']
    return render(request, 'atlas/Association.html')


def upload(request):
    return render(request, 'atlas/Upload.html')


# @require_http_methods(["GET"])
def searchQuery(request):
    # db = pymongo.MongoClient().atlas
    #
    # query = request.GET['query']
    # result = [doc for doc in db.data.find({"Product": query})]
    #
    # if result:
    #     return HttpResponse(json.dumps(result[0]), status=200)
    # else:
    #     # error = Error("product you are looking for does not exist", 404)
    #     # print(error)
    #     print("Error")
    #     return HttpResponse("Product you are looking for does not exist", status=404)
    print(request)
    # req_file = dbConfig.dict["requestUrl"]
    # req_df = pd.read_csv(req_file, encoding='utf-8')
    has_req = False
    # for i, r in req_df.iterrows():
    #     if request.GET['query'] == r['reqKw']:
    #         has_req = True
    #         break
    #     else:
    #         pass
    try:
        req1 = Requests.objects.get(reqKw=request.GET['query'])
        if len(req1) > 0:
            # has_req = True
            # if has_req:
            return HttpResponse(request.GET['query'], status=200)
        else:
            return HttpResponse("Product you are looking for does not exist", status=404)
    except:
        return HttpResponse("Product you are looking for does not exist", status=404)
    #return HttpResponse("returning from searchQuery", status=200)


@csrf_exempt
def uploadFile(request):
    print("inside uploadFile")
    #print (request)
    print (request.POST['upl_type'])
    print (request.POST['filename'])
    print ("Displaying inside views.uploadfile", request.POST['filedata'].encode('utf-8'))
    # print(type(request._files['upload'].file))
    responseObject = product_service.uploadFile(request)  # response object contains table_data

    # form = cgi.FieldStorage()
    # return HttpResponse(json.dumps([responseObject, table_data_df]), status=responseObject["status"])
    return HttpResponse(json.dumps([responseObject]), status=responseObject["status"])


def start_analysis(self):
    print("inside start_analysis")
    responseObject = product_service.start_analysis()

    return HttpResponse(json.dumps([responseObject]), status=responseObject["status"])


def read_dims(request):
    print("inside readdims")
    #print (request)
    #print dir(request)
    responseObject = product_service.read_dims(request)  # response object contains table_data
    #print(responseObject)
    #print(type(responseObject))
    return HttpResponse(json.dumps(responseObject), status=200)


def addProduct(request):
    #    return HttpResponse("added", status=200)
    JSONdata = request.POST['name']
    #print("Views -> add product request = ", JSONdata)
    site_data = request.POST['site']
    tag_dict = request.POST['tagdict']
    #site_data = request.POST.get('site', False)
    #print("Views -> add product site = ", site_data)
    #print(json.loads(site_data))
    responseObject = product_service.raiseRequest(JSONdata, json.loads(site_data), json.loads(tag_dict), False)
    return HttpResponse(json.dumps(responseObject), status=responseObject["status"])


def getRequests(request):
    print("Fetching requests queue...")
    return HttpResponse(product_service.fetchRequests(), status=200)


def getRequests1(request):
    print("Fetching requests queue")
    return HttpResponse(product_service.fetchRequests1(), status=200)


def refreshProduct(request, product_name):
    #return HttpResponse("refreshed", status=200)
    # JSONdata = request.PUT['name']
    responseObject = product_service.raiseRequest(product_name, "AM", True)
    #print("Views -> refresh product request = ", product_name)
    return HttpResponse(json.dumps(responseObject), status=responseObject["status"])


# @require_http_methods(["POST"])
# def searchQuery(request):
#     print("PUT")
#     return
#
#
# @require_http_methods(["PUT"])
# def searchQuery(request):
#     print("PUT")
#     return

def getAutoCompleteList(request):
    #return HttpResponse(json.dumps({'dict_data': static_data.product}))
    return HttpResponse(json.dumps(product_service.getMetaDataFromProducts()), status=200)


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')


def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def download_tag_file(request):
    try:
        print(request.GET['name'])
        query1 = request.GET['name']
        # curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
        # output_file_name = query1 + "_tagged_" + curr_timestamp + '.csv'
        # path1 = os.path.join(os.path.expandvars("%userprofile%"), "Desktop")
        # full_path = path1 + "\\" + output_file_name
        # print (full_path)

        has_csv = False
        dl_data = None
        if ".csv" in query1:
            has_csv = True
            query1 = query1[:len(query1) - 4]

        header_cols = ['dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6', 'dim7', 'dim8', 'dim9', 'dim10', 'dim11', 'dim12',
                    'dim13', 'dim14', 'dim15']
        headers_dict = OrderedDict((h, F(h)) for h in header_cols)
        # ngrams_list = []

        if has_csv:
            hl = DimenMap.objects.values().get(dict_filename=query1)
            for h in header_cols:
                headers_dict[hl[h]] = headers_dict.pop(h)

            dl_data = AggTaggedData.objects.values('id','dataset_filename').filter(dataset_filename=query1).annotate(article_id=F('aid_id'), **headers_dict)
            if len(dl_data) == 0:
                dl_data = AggTaggedDataUpl.objects.values('id','dataset_filename').filter(dataset_filename=query1).annotate(article_id=F('rid_id'), **headers_dict)
                # ngrams_list = TaggedDataUpl.objects.filter(dataset_filename=query1).values_list('ngram', flat=True)
            else:
                pass
                # ngrams_list = TaggedData.objects.filter(dataset_filename=query1).values_list('ngram', flat=True)
        else:
            # to find out which dict was used
            dict_name = TaggedDataRev.objects.filter(pCategory=query1).values_list('dict_filename_id', flat=True)[0:1]
            print("The dict name is > ", dict_name)

            hl = DimenMap.objects.values().get(dict_filename=dict_name)
            for h in header_cols:
                headers_dict[hl[h]] = headers_dict.pop(h)
            dl_data = AggTaggedDataRev.objects.values('id', 'pCategory').filter(pCategory=query1).annotate(rid=F('rid_id'), **headers_dict)
            # ngrams_list = TaggedDataRev.objects.filter(pCategory=query1).values_list('ngram', flat=True)
        #
        # ngrams_list = list(set(list(ngrams_list)))
        # ngrams_list = [i.encode('utf-8', 'ignore') for i in ngrams_list if not str(i) == 'None']
        # # print(ngrams_list)

        # dl_data = list(dl_data)
        # lines = [c for c in dl_data]
        # dest_url = full_path
        # fx = open(dest_url,'w')
        # w = csv.DictWriter(fx, lines[0].keys())
        # w.writeheader()
        # print(lines[0].keys())
        # for l in lines:
        #     # print(l)
        #     # fx.write(str(l)+"\n")
        #     w.writerow(l)
        # fx.close()
        # df= pd.read_csv(dest_url)
        # df = df.dropna(axis="columns", how='all')
        # df.loc[-1] = lines[0].keys()  # adding a row
        # df.index += 1  # shifting index
        # df.sort_index(inplace=True)
        # df.to_csv(dest_url, index=False)

        df = pd.DataFrame.from_records(dl_data)

        if not len(df) == 0:

            response = HttpResponse(df.to_json(orient='records'), content_type='text/csv')
            print(response)
            print(" Downloading")
            return HttpResponse(response, status=200)
        else:
            return HttpResponse(json.dumps(["Sorry! Tagged data not ready for download!"]), status=200)
    except:
        print("Error in download tagged data")
        print(traceback.print_exc())


def download_ngram_file(request):
    try:

        print(request.GET['name'])
        query1 = request.GET['name']
        has_csv = False
        if ".csv" in query1:
            has_csv = True
            query1 = query1[:len(query1) - 4]

        # curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
        # output_file_name = query1 + "_ngrams_" + curr_timestamp + '.csv'
        # path1 = os.path.join(os.path.expandvars("%userprofile%"), "Desktop")
        # full_path = path1 + "\\" + output_file_name
        # print (full_path)

        def clean_rev(curr_rev):
            curr_rev = curr_rev.replace("\n", " ").replace("\t", " ").replace("\r", " ")
            curr_rev = curr_rev.replace("&nbsp;", " ").replace("&gt;", " ").replace("&lt;", " ").replace("&quot;", " ")
            curr_rev = curr_rev.replace(" & ", " and ").replace("-", " ")
            curr_rev = re.sub(r'[^\w\s]*', "", curr_rev)  # 0 or more non-(alphanumeric or whitespace)
            curr_rev = curr_rev.strip()
            curr_rev = re.sub(r'\s{2,}', ' ', curr_rev)

            return curr_rev

        if has_csv:
            ngrams_data = Social.objects.filter(dataset_filename=query1).values('rText')

            if len(ngrams_data) == 0:
                ngrams_data = Uploads.objects.filter(pCategory=query1).values('rText')
                print("ngrams data in Uploads")
            else:
                print("ngrams data in Social")
        else:
            ngrams_data = Review.objects.filter(pid_id__pCategory=query1).values('rText')
            print("ngrams data in Review")

        df1 = pd.DataFrame.from_records(ngrams_data)
        df = pd.DataFrame({'ngram': []})
        uni_full = []
        bi_full = []
        tri_full = []

        txt_col = df1['rText']
        for t in txt_col:
            try:
                t = t.decode('utf-8', 'ignore')
                # print(t)
                curr_rev = clean_rev(t)

                trigrams = []
                bigrams = []

                unigrams = str(curr_rev).split(" ")  # for unigrams
                uni_full.extend(unigrams)

                for i in range(0, len(unigrams) - 2):  # form trigrams
                    trigrams.append(unigrams[i] + " " + unigrams[i + 1] + " " + unigrams[i + 2])
                tri_full.extend(trigrams)

                for i in range(0, len(unigrams) - 1):  # form bigrams
                    bigrams.append(unigrams[i] + " " + unigrams[i + 1])
                bi_full.extend(bigrams)
            except:
                pass

        max_l = max([len(tri_full), len(bi_full), len(uni_full)])

        while len(tri_full) < max_l:
            tri_full.append("")

        while len(bi_full) < max_l:
            bi_full.append("")

        while len(uni_full) < max_l:
            uni_full.append("")

        del df['ngram']
        df['trigrams'] = tri_full
        df['bigrams'] = bi_full
        df['unigrams'] = uni_full

        # df.to_csv(full_path, index=False, encoding='utf-8')
        print(df)
        # ngrams_data = list(ngrams_data)

        if not len(df) == 0:
            response = HttpResponse(df.to_json(orient='records'), content_type='text/csv')
            # response['Content-Disposition'] = 'attachment; filename="' + full_path + '"'
            # response['X-Sendfile'] = smart_str(full_path)
            # print(response)
            print(" Downloading")
            return HttpResponse(response, status=200)
        else:
            return HttpResponse(json.dumps(["Sorry! Ngrams not ready!"]), status=200)
    except:
        print("Error in download ngram")
        print(traceback.print_exc())


def download_contcat_data(request):
    try:
        print(request.GET['name'])
        query1 = request.GET['name']
        has_csv = False
        if ".csv" in query1:
            has_csv = True
            query1 = query1[:len(query1) - 4]

        rev_qs = None
        cc_data = None
        rid_list = []
        rtext_list = []
        if not has_csv:
            rev_qs = Review.objects.filter(pid_id__pCategory=query1).values_list('rid','rText')
            cc_data = ContentCategoryRev.objects.filter(rid_id__in=rid_list).values_list('rid_id', 'category',
                                                                                         'confidence')
        else:
            rev_qs = Uploads.objects.filter(pCategory=query1).values_list('rid','rText')
            if len(rev_qs) == 0:
                rev_qs = Social.objects.filter(dataset_filename=query1).values_list('rid', 'rText')
                cc_data = ContentCategorySoc.objects.filter(rid_id__in=rid_list).values_list('rid_id', 'category',
                                                                                             'confidence')
            else:
                cc_data = ContentCategoryUpl.objects.filter(rid_id__in=rid_list).values_list('rid_id', 'category',
                                                                                             'confidence')

        df = pd.DataFrame.from_records(cc_data)

        df['rText'] = ""

        for d in df:
            d['rText'] = next(rtext for (rid, rtext) in rev_qs if rid == d['rid_id'])

        if not len(df) == 0:
            print(df)
            response = HttpResponse(df.to_json(orient='records'), content_type='text/csv')
            print(response)
            print("Downloading")
            return HttpResponse(response, status=200)
        else:
            return HttpResponse(json.dumps(["Sorry! Content category data not ready for download!"]), status=200)
    except:
        print(traceback.print_exc())


def testscrape(request):
    print("inside testscrape")
    # # spi.run_spider()
    # try:
    #     import PyScripts.ATLAS_v2 as A2
    #     A2.main('tv set', ['am'])
    # except:
    #     print(traceback.print_exc())
    # print("scrapy spider run finish")
    rev_data = Review.objects.filter(rid__contains="tv set").values()
    print(rev_data)
    for i in rev_data:
        Analysis.objects.create(rid_id=i['rid'])
    return HttpResponse(["testscrape done"], status=200)


def download_raw_data(request):
    print(request.GET['name'])
    query1 = request.GET['name']
    # curr_timestamp = datetime.now().strftime("%d%B%Y_%I%M%S%p")
    # output_file_name = query1 + "_raw_" + curr_timestamp + '.csv'
    # path1 = os.path.join(os.path.expandvars("%userprofile%"), "Desktop")
    # full_path = path1 + "\\" + output_file_name
    # print (full_path)

    has_csv = False
    # dl_data = None
    if ".csv" in query1:
        has_csv = True
        query1 = query1[:len(query1) - 4]
    print(query1)
    if has_csv:
        raw_qs = Social.objects.filter(dataset_filename=query1).values()
        if len(raw_qs) == 0:
            raw_qs = Uploads.objects.filter(pCategory=query1).values()
            print("data in Uploads")
        else:
            print("data in Social")
    else:
        raw_qs = Review.objects.filter(pid_id__pCategory=query1).values()
        print("data in Review")

    raw_df = pd.DataFrame.from_records(raw_qs)
    # raw_df = list(raw_df)
    print(raw_df)
    if not len(raw_df) == 0:
        print(raw_df.to_json(orient='records'))
        response = HttpResponse(raw_df.to_json(orient='records'), content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="' + full_path + '"'
        # response['X-Sendfile'] = smart_str(full_path)
        # print(response)
        print(" Downloading")
        # str_msg = "Download initiated. Please check your Desktop for the file."
        return HttpResponse(response, status=200)
    else:
        return HttpResponse(["Sorry! Raw data not ready for download!"], status=200)
