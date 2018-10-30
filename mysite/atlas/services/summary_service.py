import json
import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
import django
django.setup()
from atlas.PyScripts import ATLAS1
from atlas.models import Product, Review, Analysis, Uploads, UploadAnalyses, DimenMap, TagDicts, TagDictsUpl, Social, \
    SocialAnalyses, TaggedData, TaggedDataUpl, TaggedDataRev, AggTaggedData, AggTaggedDataUpl, AggTaggedDataRev,  \
    ContentCategoryRev, ContentCategoryUpl, ContentCategorySoc
from django.db.models import Count,Avg
from django.utils.dateformat import format
import time, datetime
from atlas.config import dbConfig
from django.core import serializers
import mpld3
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import svd
import traceback


np.seterr(all='ignore', divide='ignore', invalid='ignore')


def getCountRevCards(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    if fromDate == "" or toDate == "":

        #print(brand,source,sku)
        data2 = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku) \
            .values_list('sentiment') \
            .annotate(senti_count=Count('sentiment'))

        data2_1 = Analysis.objects.filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand,
                                          rid__pid__siteCode__in=source, rid__pid__pModel__in=sku)

    else:
        data2 = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate]) \
            .values_list('sentiment') \
            .annotate(senti_count=Count('sentiment'))

        data2_1 = Analysis.objects.filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand,
                                          rid__pid__siteCode__in=source,
                                          rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate])

    #print(data2)

    count_list = list()
    totalCount = len(data2_1)
    posCount = 0
    negCount = 0

    for d in data2:
        if d[0] == "Positive":
            posCount = d[1]
        elif d[0] == "Negative":
            negCount = d[1]

    count_list.extend([totalCount, posCount, negCount])
    #print(count_list)
    data_json = json.dumps(count_list, cls=DjangoJSONEncoder)
    return data_json


def getCountRevCardsOverall(kw):
    kw = str(kw)[:len(kw) - 4]

    test = Uploads.objects.filter(pCategory=kw).values()
    if test:
        rid_list = Uploads.objects.filter(pCategory=kw).values_list('rid')
        rid_list = list(set(rid_list))
        #print(rid_list)
        data2 = UploadAnalyses.objects.filter(rid_id__in=rid_list).values_list('sentiment') \
            .annotate(senti_count=Count('sentiment'))

        #print(data2)

        data2_1 = UploadAnalyses.objects.filter(rid_id__in=rid_list)
    else:
        aid_list = Social.objects.filter(dataset_filename=kw).values_list('aid', flat=True)
        aid_list = list(set(aid_list))
        #print(aid_list)
        data2 = SocialAnalyses.objects.filter(aid_id__in=aid_list).values_list('sentiment') \
            .annotate(senti_count=Count('sentiment'))

        #print(data2)

        data2_1 = SocialAnalyses.objects.filter(aid_id__in=aid_list)

    count_list = list()
    totalCount = len(data2_1)
    posCount = 0
    negCount = 0

    for d in data2:
        if d[0] == "Positive":
            posCount = d[1]
        elif d[0] == "Negative":
            negCount = d[1]

    count_list.extend([totalCount, posCount, negCount])
    data_json = json.dumps(count_list)
    return data_json


def getTopposPosts(kw, brand, source, sku, fromDate, toDate, topn):
    # print(kw, brand, source, sku, fromDate, toDate, topn)
    topn = int(str(topn).split(" ")[1])

    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    # print(source1)
    source = source1

    p_flag = False  # set true if no records tagged positive

    if fromDate == "" or toDate == "":

        top_pos_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, sentiment='Positive') \
            .order_by('-sentiScore') \
            .values_list('rid_id', flat=True)[:topn]
        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        if not top_pos_ids1:
            print("No records tagged positive!!")
            p_flag = True

        if not p_flag:  # if there are positive reviews
            pos_data = Review.objects.filter(rid__in=top_pos_ids1).only('rTitle', 'rText')
            #print(pos_data)
            data1 = serializers.serialize("json", pos_data)
            data_json = json.dumps(data1, cls=DjangoJSONEncoder)
            return data_json
        else:
            return

    else:

        top_pos_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate], sentiment='Positive') \
            .order_by('-sentiScore') \
            .values_list('rid_id', flat=True)[:topn]
        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        if not top_pos_ids1:
            #print("No records were tagged positive!")
            p_flag=True

        if not p_flag:
            pos_data = Review.objects.filter(rid__in=top_pos_ids1).only('rTitle', 'rText')
            #print(pos_data)

            data1 = serializers.serialize("json", pos_data)
            data_json = json.dumps(data1, cls=DjangoJSONEncoder)
            return data_json
        else:
            return


def getTopposPostsOverall(kw, topn):
    kw = str(kw)[:len(kw) - 4]
    topn = int(str(topn).split(" ")[1])

    test = Uploads.objects.filter(pCategory=kw).values()
    if test:
        top_pos_ids = UploadAnalyses.objects.filter(rid__pCategory=kw, sentiment='Positive').order_by('-sentiScore') \
                          .values_list('rid_id', flat=True)[:topn]
        top_pos_ids1 = list(top_pos_ids)
        # print(top_pos_ids1)

        pos_data = Uploads.objects.filter(rid__in=top_pos_ids1).only('rTitle', 'rText')
        # print(pos_data)

        data1 = serializers.serialize("json", pos_data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json

    else:
        top_pos_ids = SocialAnalyses.objects.filter(aid__dataset_filename=kw, sentiment='Positive').order_by(
            '-sentiScore') \
                          .values_list('aid_id', flat=True)[:topn]

        top_pos_ids1 = list(top_pos_ids)
        # print(top_pos_ids1)

        pos_data = Social.objects.filter(aid__in=top_pos_ids1).only('rTitle', 'rText')
        # print(pos_data)

        data1 = serializers.serialize("json", pos_data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json


def getTopnegPosts(kw, brand, source, sku, fromDate, toDate, topn):
    topn = int(str(topn).split(" ")[1])

    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    n_flag = False  # set true if no records tagged positive

    if fromDate == "" or toDate == "":

        top_neg_ids = Analysis.objects \
                          .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                                  rid__pid__pModel__in=sku, sentiment='Negative') \
                          .order_by('sentiScore') \
                          .values_list('rid_id', flat=True)[:topn]
        top_neg_ids1 = list(top_neg_ids)
        # print(top_neg_ids1)

        if not top_neg_ids1:
            print("No records tagged negative!!")
            n_flag = True

        if not n_flag:
            neg_data = Review.objects.filter(rid__in=top_neg_ids1).only('rTitle', 'rText')
            # print(neg_data)
            data1 = serializers.serialize("json", neg_data)
            data_json = json.dumps(data1, cls=DjangoJSONEncoder)
            return data_json
        else:
            return

    else:

        top_neg_ids = Analysis.objects \
                          .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                                  rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate], sentiment='Negative') \
                          .order_by('sentiScore') \
                          .values_list('rid_id', flat=True)[:topn]
        top_neg_ids1 = list(top_neg_ids)
        # print(top_neg_ids1)

        if not top_neg_ids1:
            print("No records were tagged negative!")
            n_flag = True

        if not n_flag:
            neg_data = Review.objects.filter(rid__in=top_neg_ids1).only('rTitle', 'rText')
            # print(neg_data)

            data1 = serializers.serialize("json", neg_data)
            data_json = json.dumps(data1, cls=DjangoJSONEncoder)
            return data_json
        else:
            return


def getTopnegPostsOverall(kw, topn):
    kw = str(kw)[:len(kw) - 4]
    topn = int(str(topn).split(" ")[1])

    test = Uploads.objects.filter(pCategory=kw).values()
    if test:
        top_neg_ids = UploadAnalyses.objects.filter(rid__pCategory=kw, sentiment='Negative').order_by('sentiScore') \
                          .values_list('rid_id', flat=True)[:topn]
        top_neg_ids1 = list(top_neg_ids)
        # print(top_neg_ids1)

        neg_data = Uploads.objects.filter(rid__in=top_neg_ids1).only('rTitle', 'rText')
        # print(neg_data)

        data1 = serializers.serialize("json", neg_data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json

    else:
        top_neg_ids = SocialAnalyses.objects.filter(aid__dataset_filename=kw, sentiment='Negative').order_by(
            'sentiScore') \
                          .values_list('aid_id', flat=True)[:topn]
        top_neg_ids1 = list(top_neg_ids)
        # print(top_neg_ids1)

        neg_data = Social.objects.filter(aid__in=top_neg_ids1).only('rTitle', 'rText')
        # print(neg_data)

        data1 = serializers.serialize("json", neg_data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json


def getTopposneg(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    p_flag = False  # set true if no records tagged positive
    n_flag = False  # set to True if no records tagged negative
    pos_data = None
    neg_data = None
    if fromDate == "" or toDate == "":

        top_pos_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, sentiment='Positive') \
            .order_by('-sentiScore') \
            .values_list('rid_id', flat=True)[:2]
        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        if not top_pos_ids1:
            print("No records tagged positive!!")
            p_flag = True

        if not p_flag:  # if there are positive reviews
            pos_data = Review.objects.filter(rid__in=top_pos_ids1).only('rTitle', 'rText')
            #print(pos_data)

        top_neg_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, sentiment='Negative') \
            .order_by('sentiScore') \
            .values_list('rid_id', flat=True)[:2]
        top_neg_ids1 = list(top_neg_ids)
        #print(top_neg_ids1)

        if not top_neg_ids1:
            print("No records tagged negative!!")
            n_flag = True

        if not n_flag:
            neg_data = Review.objects.filter(rid__in=top_neg_ids1).only('rTitle', 'rText')
            #print(neg_data)

    else:

        top_pos_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate], sentiment='Positive') \
            .order_by('-sentiScore') \
            .values_list('rid_id', flat=True)[:2]
        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        if not top_pos_ids1:
            #print("No records were tagged positive!")
            p_flag=True

        if not p_flag:
            pos_data = Review.objects.filter(rid__in=top_pos_ids1).only('rTitle', 'rText')
            #print(pos_data)

        top_neg_ids = Analysis.objects \
            .filter(rid__pid__pCategory=kw, rid__pid__pBrand__in=brand, rid__pid__siteCode__in=source,
                    rid__pid__pModel__in=sku, rid__rDate2__range=[fromDate, toDate], sentiment='Negative') \
            .order_by('sentiScore') \
            .values_list('rid_id', flat=True)[:2]
        top_neg_ids1 = list(top_neg_ids)
        #print(top_neg_ids1)

        if not top_neg_ids1:
            print("No records were tagged negative!")
            n_flag = True

        if not n_flag:
            neg_data = Review.objects.filter(rid__in=top_neg_ids1).only('rTitle', 'rText')
            #print(neg_data)

    if not p_flag and not n_flag:
        data = pos_data.union(neg_data)
        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json
    elif not p_flag and n_flag:
        data = pos_data
        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json
    elif p_flag and not n_flag:
        data = neg_data
        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json
    else:
        print("No data to show!")
        data = []
        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json


class CA(object):
    """Simple correspondence analysis.

    Inputs
     ------
    ct : array_like

      Two-way contingency table. If `ct` is a pandas DataFrame object,
      the index and column values are used for plotting.

    Notes
    -----
    The implementation follows that presented in 'Correspondence
    Analysis in R, with Two- and Three-dimensional Graphics: The ca
    Package,' Journal of Statistical Software, May 2007, Volume 20,
    Issue 3.

    """

    def __init__(self, ct):
        self.rows = ct.index.values if hasattr(ct, 'index') else None
        self.cols = ct.columns.values if hasattr(ct, 'columns') else None

        # contingency table
        N = np.matrix(ct, dtype=float)

        # correspondence matrix from contingency table
        # try:
        # np.seterr(divide='ignore', invalid='ignore')
        P = N / N.sum()
        # except:

        # row and column marginal totals of P as vectors
        r = P.sum(axis=1)
        c = P.sum(axis=0).T

        # diagonal matrices of row/column sums
        D_r_rsq = np.diag(1. / np.sqrt(r.A1))
        D_c_rsq = np.diag(1. / np.sqrt(c.A1))

        # the matrix of standarized residuals
        S = D_r_rsq * (P - r * c.T) * D_c_rsq

        # compute the SVD
        U, D_a, V = svd(S, full_matrices=False)
        D_a = np.asmatrix(np.diag(D_a))
        V = V.T

        # principal coordinates of rows
        F = D_r_rsq * U * D_a

        # principal coordinates of columns
        G = D_c_rsq * V * D_a

        # standard coordinates of rows
        X = D_r_rsq * U

        # standard coordinates of columns
        Y = D_c_rsq * V

        # the total variance of the data matrix
        inertia = sum([(P[i, j] - r[i, 0] * c[j, 0]) ** 2 / (r[i, 0] * c[j, 0])
                       for i in range(N.shape[0])
                       for j in range(N.shape[1])])

        self.F = F.A
        self.G = G.A
        self.X = X.A
        self.Y = Y.A
        self.inertia = inertia
        self.eigenvals = np.diag(D_a) ** 2

    def plot(self):
        """Plot the first and second dimensions."""
        xmin, xmax = None, None
        ymin, ymax = None, None
        if self.rows is not None:
            for i, t in enumerate(self.rows):
                x, y = self.F[i, 0], self.F[i, 1]
                plt.text(x, y, t, va='center', ha='center', color='r')
                xmin = min(x, xmin if xmin else x)
                xmax = max(x, xmax if xmax else x)
                ymin = min(y, ymin if ymin else y)
                ymax = max(y, ymax if ymax else y)
        else:
            plt.plot(self.F[:, 0], self.F[:, 1], 'ro')

        if self.cols is not None:
            for i, t in enumerate(self.cols):
                x, y = self.G[i, 0], self.G[i, 1]
                plt.text(x, y, t, va='center', ha='center', color='b')
                xmin = min(x, xmin if xmin else x)
                xmax = max(x, xmax if xmax else x)
                ymin = min(y, ymin if ymin else y)
                ymax = max(y, ymax if ymax else y)
        else:
            plt.plot(self.G[:, 0], self.G[:, 1], 'bs')

        if xmin and xmax:
            pad = (xmax - xmin) * 0.1
            plt.xlim(xmin - pad, xmax + pad)
        if ymin and ymax:
            pad = (ymax - ymin) * 0.1
            plt.ylim(ymin - pad, ymax + pad)

        plt.grid()
        plt.xlabel('Dim 1')
        plt.ylabel('Dim 2')

    def scree_diagram(self, perc=True, *args, **kwargs):
        """Plot the scree diagram."""
        eigenvals = self.eigenvals
        xs = np.arange(1, eigenvals.size + 1, 1)
        ys = 100. * eigenvals / eigenvals.sum() if perc else eigenvals
        plt.plot(xs, ys, *args, **kwargs)
        plt.xlabel('Dimension')
        plt.ylabel('Eigenvalue' + (' [%]' if perc else ''))


def getPivotcontent(kw):
    # print("pivot", kw)
    has_csv = False

    if ".csv" in kw:
        has_csv = True
        kw = str(kw).split(".")[0]
        # print(kw)
    # print(kw)
    # print("has_csv", has_csv)

    # all_cols = ATLAS1.gen_all_cols()

    all_cols = ['rid', 'rid_id__rDate2', 'rid_id__dt', 'rid_id__mth', 'rid_id__year', 'dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6', 'dim7', 'dim8', 'dim9', 'dim10', 'dim11', 'dim12',
                'dim13', 'dim14', 'dim15', 'rid_id__rRating', 'rid_id__rText', 'rid_id__rTitle', 'rid_id__rUser']
    # all_cols = ['dim1', 'dim2','dim3', 'dim4', 'dim5', 'dim6', 'dim7',
    #                 'dim8', 'dim9', 'dim10', 'dim11', 'dim12','dim13',
    #                 'dim14', 'dim15', 'd1_l1', 'd1_l2','d1_l3','d1_l4','d1_l5',
    #                 'd2_l1', 'd2_l2', 'd2_l3', 'd2_l4', 'd2_l5', 'd3_l1',
    #                 'd3_l2', 'd3_l3', 'd3_l4', 'd3_l5', 'd4_l1', 'd4_l2',
    #                 'd4_l3', 'd4_l4', 'd4_l5', 'd6_l1', 'd6_l2', 'd6_l3',
    #                 'd6_l4', 'd6_l5', 'd7_l1', 'd7_l2', 'd7_l3', 'd7_l4',
    #                 'd7_l5', 'd8_l1', 'd8_l2', 'd8_l3', 'd8_l4', 'd8_l5',
    #                 'd9_l1', 'd9_l2', 'd9_l3', 'd9_l4', 'd9_l5', 'd10_l1',
    #                 'd10_l2', 'd10_l3', 'd10_l4', 'd10_l5', 'd11_l1',
    #                 'd11_l2', 'd11_l3', 'd11_l4', 'd11_l5','d12_l1',
    #                 'd12_l2', 'd12_l3', 'd12_l4', 'd12_l5', 'd13_l1',
    #                 'd13_l2', 'd13_l3', 'd13_l4', 'd13_l5', 'd14_l1',
    #                 'd14_l2', 'd14_l3', 'd14_l4', 'd14_l5', 'd15_l1',
    #                 'd15_l2', 'd15_l3', 'd15_l4', 'd15_l5']

    in_AggTaggedDataRev = False

    if has_csv:
        data = AggTaggedData.objects.filter(dataset_filename=kw).values('rid', 'aid_id__rDate2', 'aid_id__dt', 'aid_id__mth', 'aid_id__year', 'dim1', 'dim2','dim3', 'dim4', 'dim5', 'dim6', 'dim7',
                                                                        'dim8', 'dim9', 'dim10', 'dim11', 'dim12','dim13',
                                                                        'dim14', 'dim15', 'aid_id__rRating', 'aid_id__rText', 'aid_id__rTitle', 'aid_id__rUser')
        data_rids = AggTaggedData.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
        cc_data = ContentCategorySoc.objects.filter(rid_id__in=data_rids).values()

        if len(data) == 0:
            data = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values('rid_id', 'rid_id__rDate2', 'rid_id__dt', 'rid_id__mth', 'rid_id__year', 'dim1', 'dim2', 'dim3', 'dim4', 'dim5',
                                                                                'dim6',
                                                                                'dim7', 'dim8', 'dim9', 'dim10',
                                                                                'dim11', 'dim12',
                                                                                'dim13', 'dim14', 'dim15', 'rid_id__rRating', 'rid_id__rText', 'rid_id__rTitle',
                                                                                'rid_id__rUser')

            print("Data in AggTaggedDataUpl")
            # print(data)
        else:
            print("Data in AggTaggedData")

    else:
        data = AggTaggedDataRev.objects.filter(pCategory=kw).values('rid_id', 'rid_id__rDate2', 'rid_id__dt', 'rid_id__mth', 'rid_id__year', 'dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6',
                                                                     'dim7','dim8', 'dim9', 'dim10', 'dim11', 'dim12', 'dim13',
                                                                     'dim14', 'dim15', 'rid_id__rRating', 'rid_id__rText', 'rid_id__rTitle', 'rid_id__rUser')
        data_rids = AggTaggedDataRev.objects.filter(pCategory=kw).values_list('rid_id',flat=True)
        cc_qs = ContentCategoryRev.objects.filter(rid_id__in=data_rids).values('rid_id', 'category_pri', 'category_sec', 'category_ter')
        # print(cc_qs)
        # print([c for c in cc_qs])
        cc_data = [{'rid_id': c['rid_id'], 'category_pri': c['category_pri'], 'category_sec': c['category_sec'], 'category_ter': c['category_ter']} for c in cc_qs]
        # print(cc_data)
        in_AggTaggedDataRev = True
        print("Data in AggTaggedDataRev")

    data1 = []
    try:
        if in_AggTaggedDataRev:
            dict_name = TaggedDataRev.objects.filter(dict_filename_id=kw).values_list('dict_filename_id', flat=True)[0:1]
            if not len(dict_name) > 0:
                dict_name = 'speakers_1'
                print("dictname ", dict_name)
                data1 = DimenMap.objects.values().get(dict_filename=dict_name)
                if not len(data1) > 0:
                    dict_name = 'kelloggs_1'
                    print("dictname ", dict_name)
                    data1 = DimenMap.objects.values().get(dict_filename=dict_name)

        else:
            data1 = DimenMap.objects.values().get(dict_filename=kw)

            if len(data1) == 0:
                data1 = DimenMap.objects.values().get(dict_filename='speakers_1')  # default dict

    except:
        # print(traceback.print_exc())
        data1 = DimenMap.objects.values().get(dict_filename='speakers_1')  # default dict

    # print(type(data))

    for d in data:
        # print d
        for i in all_cols:
            # print i
            # print data1[i]
            if i not in ['rid', 'rid_id', 'rid_id__rDate2', 'rid_id__dt', 'rid_id__rRating', 'rid_id__rText', 'rid_id__rTitle',
                         'rid_id__rUser', 'rid_id__mth', 'rid_id__year', 'aid_id__rDate2', 'aid_id__dt', 'aid_id__mth',
                         'aid_id__year']:
                d[str(data1[i]).title()] = d.pop(i)
            elif i in ['rid', 'rid_id']:
                d['Review ID'] = d.pop(i)
            elif i == 'rid_id__rRating' or i == 'aid_id__rRating':
                d['Rating'] = d.pop(i)
            elif i == 'rid_id__rText' or i == 'aid_id__rText':
                d['Text'] = d.pop(i)
            elif i == 'rid_id__rTitle' or i == 'aid_id__rTitle':
                d['Title'] = d.pop(i)
            elif i == 'rid_id__rUser' or i == 'aid_id__rUser':
                d['User/Author'] = d.pop(i)
            elif i in ['rid_id__rDate2', 'aid_id__rDate2']:
                try:
                    d['Date'] = d.pop('rid_id__rDate2')
                except:
                    d['Date'] = d.pop('aid_id__rDate2')
            elif i in ['rid_id__dt', 'aid_id__dt']:
                try:
                    d['DD'] = d.pop('rid_id__dt')
                except:
                    d['DD'] = d.pop('aid_id__dt')
            elif i in ['rid_id__mth', 'aid_id__mth']:
                try:
                    d['MM'] = d.pop('rid_id__mth')
                except:
                    d['MM'] = d.pop('aid_id__mth')
            elif i in ['rid_id__year', 'aid_id__year']:
                try:
                    d['YYYY'] = d.pop('rid_id__year')
                except:
                    d['YYYY'] = d.pop('aid_id__year')

        # for i in range(len(cc_data)):
        #     if cc_data[i]['rid_id'] == d['Review ID']:
        #         d['Primary Content Category'] = cc_data[i]['category_pri']
        #         d['Secondary Content Category'] = cc_data[i]['category_sec']
        #         d['Tertiary Content Category'] = cc_data[i]['category_ter']
        #         break
    list_data = list(data)

    # CODE FOR EXTENDING DATA--->
    final_list_data = []

    cat_list = [c['rid_id'] for c in cc_data]
    # print(cat_list)

    agg_list = [ld['Review ID'] for ld in list_data]
    # print(agg_list)

    nonmatch = [c for c in cat_list if not c in agg_list]
    # print(nonmatch)

    dim_cols_list = ['dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6', 'dim7', 'dim8', 'dim9', 'dim10', 'dim11', 'dim12',
                     'dim13', 'dim14', 'dim15']

    for c in cc_data:
        if c['rid_id'] in nonmatch:
            tempdict = dict((d, None) for d in dim_cols_list)
            tempdict.update(c)
            final_list_data.append(tempdict)
        else:
            # print("c=", c)
            for ld in list_data:
                # print("a=", a)
                if c['rid_id'] == ld['Review ID']:
                    tempdict = ld.copy()
                    tempdict['Primary Content Category'] = c['category_pri']
                    tempdict['Secondary Content Category'] = c['category_sec']
                    tempdict['Tertiary Content Category'] = c['category_ter']
                    # print("tempdict=", tempdict)
                    final_list_data.append(tempdict)
                    # print("fintab=", fintab)

    print("Printing fintab")
    # print(fintab)
    # for f in fintab:


    # for ld in list_data:
    #     for i in range(len(cc_data)):
    #         # if cc_data[i]['rid_id'] == ld['Review ID']:
    #         ld['Primary Content Category'] = cc_data[i]['category_pri']
    #         ld['Secondary Content Category'] = cc_data[i]['category_sec']
    #         ld['Tertiary Content Category'] = cc_data[i]['category_ter']
    pd_df = pd.DataFrame(final_list_data)
    # pd_df.to_csv("C:\Users\\akshat.gupta\Desktop\pivotdata_new.csv",encoding='utf-8',header=True)
    # print(pd_df)
    # data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    data_json = json.dumps(final_list_data, cls=DjangoJSONEncoder)

    #print("Data_json is : neo -- ", data_json)
    return data_json


def getAssocDims(kw):
    print("inside getassocdims")
    kw1 = kw
    is_scraped = False
    if ".csv" in kw:
        is_scraped = False
        kw = kw[:len(kw) - 4]
    else:
        is_scraped = True
    print(kw)

    try:
        data1 = DimenMap.objects.values().get(dict_filename=kw)
        print("dimenmap kw")
    except:
        dict_name = ""
        if is_scraped:
            dict_name = TaggedDataRev.objects.filter(pCategory=kw).values_list('dict_filename_id', flat=True)[0:1]
            print("dict_name===>", dict_name)
        else:
            try:
                dict_name = TagDicts.objects.filter(dict_filename=kw)[0:1].values_list('dict_filename_id', flat=True)
            except:
                dict_name = TagDictsUpl.objects.filter(dict_filename=kw)[0:1].values_list('dict_filename_id', flat=True)
        print("dict_name", dict_name)

        try:
            data1 = DimenMap.objects.values().get(dict_filename=dict_name)
            print("dimenmap dictname", dict_name)
            # if len(data1) == 0:
            #     data1 = DimenMap.objects.values().get(dict_filename='speakers_1')
            #     print("dimenmap default")
            # else:
            #     print("dimenmap dictname")
        except:

            data1 = DimenMap.objects.values().get(dict_filename='speakers_1')
            print("dimenmap default")

        #return json.dumps([], cls=DjangoJSONEncoder)

    dims = []

    for k, v in data1.iteritems():
        if not k == "id" and not k == "dict_filename" and not "_" in k and len(v) > 1 and not v.lower() == "brand":
            #print(v)
            dims.append(v)
    # print(dims)


    #print(type(dims))
    data_json = json.dumps(dims, cls=DjangoJSONEncoder)
    return data_json


def getAssocLevels(kw, dim):
    # print("inside getassoclevels")
    # print(dim)
    try:
        data1 = DimenMap.objects.values().get(dict_filename=kw)
        print("dimenmap kw")
    except:
        data1 = DimenMap.objects.values().get(dict_filename='speakers_1')
        print("dimenmap default")
        # data1 = data1[0]
    dim_col = ""
    level_cols = []

    for k, v in data1.iteritems():

        if v == dim:
            dim_col = k

    x = dim_col[dim_col.index("m") + 1:]  # extract dim number
    for i in range(1, 6):
        level_cols.append("d" + x + "_l" + str(i))
    # print(level_cols)

    levels_dict = dict((l, "") for l in level_cols)
    for k, v in data1.iteritems():
        for l in level_cols:
            if k == l:
                levels_dict[l] = v
    #print(levels_dict)

    levels = list(set(levels_dict.values()))
    levels = [x for x in levels if not x == " "]
    #print(levels)
    data_json = json.dumps(levels, cls=DjangoJSONEncoder)
    return data_json


def get_assoc_values1(kw, dim, lev):  # uses
    # print(dim, lev)
    has_csv = False
    if ".csv" in kw:
        has_csv = True
        kw = str(kw).split(".")[0]

    if lev == dim:
        print("This dimension has no levels. Using the dimension itself.")

    try:
        data1 = DimenMap.objects.values().get(dict_filename=kw)
    except:
        data1 = DimenMap.objects.filter(dict_filename=kw).values()[0:1]
        data1 = data1[0]
    brand_col = ""
    lev_col = ""
    dim_col = ""

    #print(data1)
    for k, v in data1.iteritems():
        if v.lower() == "brand":
            brand_col = k
        if v == dim:
            dim_col = k
            #print(dim_col)

    if lev == dim:
        lev_col = dim_col
    else:
        for k, v in data1.iteritems():
            if v == lev and str(k).split("_")[0][1:] == dim_col[dim_col.index('m') + 1:]:
                lev_col = k

    # print(brand_col)
    #print(dim_col)
    #print(lev_col)

    if has_csv:
        brands = AggTaggedData.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
        if len(brands) == 0:
            brands = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
            # print("brands in AggTaggedDataUpl")
        else:
            pass
            # print("brands in AggTaggedData")
    else:
        brands = AggTaggedDataRev.objects.filter(pCategory=kw).values_list(brand_col, flat=True)
        # print("brands in AggTaggedDataRev")
    brands = list(set(brands))
    #brands = [x for x in brands if str(x) != 'nan']
    # print(brands)

    if has_csv:
        levs = AggTaggedData.objects.filter(dataset_filename=kw).values_list(lev_col, flat=True)
        if len(levs) == 0:
            levs = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list(lev_col, flat=True)
            # print("levels in AggTaggedDataUpl")
        else:
            pass
            # print("levels in AggTaggedData")
    else:
        levs = AggTaggedDataRev.objects.filter(dataset_filename=kw).values_list(lev_col, flat=True)
        # print("levels in AggTaggedDataRev")
    levs = list(set(levs))
    levs = [x for x in levs if str(x) != ' ']
    # print(levs)

    # Form dataframe to hold values
    if len(brands) > 0 and len(levs) > 0:
        # print("len(brands) > 0 and len(levs) > 0")
        data_df = pd.DataFrame({'brand': brands})
        # print(data_df)
        for l in levs:
            data_df[l] = 0
        # print(data_df)

        # Fill in values

        if has_csv:
            rids = AggTaggedData.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
            if len(rids) == 0:
                rids = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
                # print("rids in TaggedDataUpl")
            else:
                pass
                # print("rids in TaggedData")
        else:
            rids = AggTaggedDataRev.objects.filter(pCategory=kw).values_list('rid', flat=True)
            # print("rids in TaggedDataRev")
        rids = list(set(rids))
        # print(rids)

        for r in rids:
            if has_csv:
                data2 = AggTaggedData.objects.filter(dataset_filename=kw, rid=r).values(brand_col, lev_col)
                if len(data2) == 0:
                    data2 = AggTaggedDataUpl.objects.filter(dataset_filename=kw, rid=r).values(brand_col, lev_col)
                    print("data2 in AggTaggedDataUpl")
                else:
                    print("data2 in AggTaggedData")
                    pass
            else:
                data2 = AggTaggedDataRev.objects.filter(pCategory=kw, rid=r).values(brand_col, lev_col)
                print("data2 in AggTaggedDataRev")
            data2 = list(data2)
            # print(data2)

            print("forming data_df")
            for b in brands:
                for l in levs:
                    bl_check = [False, False]

                    for d in range(len(data2)):
                        if b in data2[d].values() or l in data2[d].values():
                            if b in data2[d].values():
                                bl_check[0] = True
                            if l in data2[d].values():
                                bl_check[1] = True
                    if bl_check == [True, True]:
                        #print(b, l)
                        data_df.ix[data_df['brand'] == b, data_df.columns[data_df.columns.get_loc(l)]] += 1
                    #print(bl_check)
            print("data_df formed")
    else:
        data_df = []
        print("data_df not formed. returning empty data_df")
    # print(data_df)

    return data_df


def get_assoc_values(kw, dim):  # uses aggtaggeddata to load only dimensions
    print("inside get_assoc_values")
    # print(dim)
    # print(kw)
    if ".csv" in kw:
        is_scraped = False
        kw = str(kw).split(".")[0]
    else:
        is_scraped = True

    if is_scraped:
        check_filepath = dbConfig.dict['dbfolderPath'] + kw + "_brand_" + dim + ".csv"
    else:
        check_filepath = dbConfig.dict['dbfolderPath'] + kw + "-csv_brand_" + dim + ".csv"

    try:
        check_file = pd.read_csv(check_filepath)
        is_data_generated = True
    except:
        is_data_generated = False

    # print("is data generated flag = ", is_data_generated)
    if not is_data_generated:
        try:
            data1 = DimenMap.objects.values().get(dict_filename=kw)
            # print("dimenmap kw")
        except:
            dict_name = ""
            if is_scraped:
                dict_name = TaggedDataRev.objects.filter(pCategory=kw).values_list('dict_filename_id', flat=True)[0:1]
            else:
                try:
                    dict_name = TagDicts.objects.filter(dict_filename=kw).values_list('dict_filename_id', flat=True)[0:1]
                except:
                    dict_name = TagDictsUpl.objects.filter(dict_filename=kw).values_list('dict_filename_id', flat=True)[0:1]
            print("dict_name", dict_name)
            try:
                data1 = DimenMap.objects.values().get(dict_filename=dict_name)
                print("dimenmap dictname", dict_name)
                # if len(data1) == 0:
                #     data1 = DimenMap.objects.values().get(dict_filename='speakers_1')
                #     print("dimenmap default")
                # else:
                #     print("dimenmap dictname")
            except:
                data1 = DimenMap.objects.values().get(dict_filename='speakers_1')
                # print("dimenmap default")

        brand_col = ""
        # lev_col = ""
        dim_col = ""

        #print(data1)
        for k, v in data1.iteritems():
            if v.lower() == "brand":
                brand_col = k
            if v == dim:
                dim_col = k
                #print(dim_col)

        # if lev == dim:
        #     lev_col = dim_col
        # else:
        #     for k, v in data1.iteritems():
        #         if v == lev and str(k).split("_")[0][1:] == dim_col[dim_col.index('m') + 1:]:
        #             lev_col = k

        # print("brand col: ",brand_col)
        # print("dim col: ", dim_col)

        if not is_scraped:
            brands = AggTaggedData.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
            if len(brands) == 0:
                brands = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
                # print("brands in AggTaggedDataUpl")
            else:
                print("brands in AggTaggedData")

        else:
            brands = AggTaggedDataRev.objects.filter(pCategory=kw).values_list(brand_col, flat=True)
            print("brands in AggTaggedDataRev")
        brands = list(set(brands))
        #brands = [x for x in brands if str(x) != 'nan']
        # print(brands)

        if not is_scraped:
            dims = AggTaggedData.objects.filter(dataset_filename=kw).values_list(dim_col, flat=True)
            if len(dims) == 0:
                dims = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list(dim_col, flat=True)
                # print("dims in AggTaggedDataUpl")
            else:
                print("dims in AggTaggedData")
        else:
            dims = AggTaggedDataRev.objects.filter(pCategory=kw).values_list(dim_col, flat=True)
            # print("dims in AggTaggedDataRev")
        dims = list(set(dims))
        # print(dims)
        dims = [x for x in dims if str(x) != ' ']
        # print(dims)

        # Form dataframe to hold values
        if len(brands) > 0 and len(dims) > 0:
            # print("len(brands) > 0 and len(dims) > 0")
            data_df = pd.DataFrame({'brand': brands})
            # print(data_df)
            for d in dims:
                data_df[d] = 0
            # print(data_df)

            # Fill in values

            if not is_scraped:
                rids = AggTaggedData.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
                if len(rids) == 0:
                    rids = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
                    # print("rids in TaggedDataUpl")
                else:
                    print("rids in TaggedData")
            else:
                rids = AggTaggedDataRev.objects.filter(pCategory=kw).values_list('rid', flat=True)
                # print("rids in TaggedDataRev")
            rids = list(set(rids))
            # print(rids)

            for r in rids:
                if not is_scraped:
                    data2 = AggTaggedData.objects.filter(dataset_filename=kw, rid=r).values(brand_col, dim_col)
                    if len(data2) == 0:
                        data2 = AggTaggedDataUpl.objects.filter(dataset_filename=kw, rid=r).values(brand_col, dim_col)
                        # print("data2 in AggTaggedDataUpl")
                    else:
                        # print("data2 in AggTaggedData")
                        pass
                else:
                    data2 = AggTaggedDataRev.objects.filter(pCategory=kw, rid=r).values(brand_col, dim_col)
                    # print("data2 in AggTaggedDataRev")
                data2 = list(data2)
                # print(data2)

                # print("forming data_df")
                # print(brands)
                # print(dims)
                for b in brands:
                    for d in dims:
                        bd_check = [False, False]

                        for d1 in range(len(data2)):
                            if b in data2[d1].values() or d in data2[d1].values():
                                if b in data2[d1].values():
                                    bd_check[0] = True
                                if d in data2[d1].values():
                                    bd_check[1] = True
                        if bd_check == [True, True]:
                            # print(b, d)
                            # print(data_df.columns[data_df.columns.get_loc(d)])
                            data_df.ix[data_df['brand'] == b, data_df.columns[data_df.columns.get_loc(d)]] += 1
                        #print(bl_check)
                # print("data_df formed")
            # print("for done")
            if is_scraped:
                data_df.to_csv(dbConfig.dict['dbfolderPath'] + kw + "_brand_" + dim + ".csv", index=False)
            else:
                data_df.to_csv(dbConfig.dict['dbfolderPath'] + kw + "-csv_brand_" + dim + ".csv", index=False)
        else:
            data_df = []
            print("data_df not formed. returning empty data_df")
        print("data_df done")
    else:
        check_file = pd.read_csv(check_filepath)
        data_df = check_file

    return data_df


def bl_check(curr_dict, b, l):

    bl_flag = [False, False]
    return bl_flag


# def get_assoc_values(kw, dim, lev):   # for dimen n levels from aggtaggeddata  + taggeddata
#     print(dim, lev)
#     has_csv = False
#     if ".csv" in kw:
#         has_csv = True
#         kw = str(kw).split(".")[0]
#
#     if lev == dim:
#         print("This dimension has no levels. Using the dimension itself.")
#
#     try:
#         data1 = DimenMap.objects.values().get(dict_filename=kw)
#         print("dimenmap kw")
#     except:
#         data1 = DimenMap.objects.values().get(dict_filename="kelloggs_1")
#         print("dimenmap default")
#         # data1 = data1[0]
#     brand_col = ""
#     lev_col = ""
#     dim_col = ""
#
#     #print(data1)
#     for k, v in data1.iteritems():
#         if v.lower() == "brand":
#             brand_col = k
#         if v == dim:
#             dim_col = k
#             #print(dim_col)
#
#     if lev == dim:
#         lev_col = dim_col
#     else:
#         for k, v in data1.iteritems():
#             if v == lev and str(k).split("_")[0][1:] == dim_col[dim_col.index('m') + 1:]:
#                 lev_col = k
#
#     print("brand_col", brand_col)
#     print("dimcol", dim_col)
#     print("levcol", lev_col)
#
#     if has_csv:
#         brands = AggTaggedData.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
#         if len(brands) == 0:
#             brands = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list(brand_col, flat=True)
#             print("brands in AggTaggedDataUpl")
#         else:
#             print("brands in AggTaggedData")
#     else:
#         brands = AggTaggedDataRev.objects.filter(pCategory=kw).values_list(brand_col, flat=True)
#         print("brands in AggTaggedDataRev")
#     brands = list(set(brands))
#     #brands = [x for x in brands if str(x) != 'nan']
#     print(brands)
#
#     table_name = "None"
#     if has_csv:
#         levs = TagDicts.objects.filter(dict_filename=kw).values_list(lev_col, flat=True)
#         if len(levs) == 0:
#             levs = TagDictsUpl.objects.filter(dataset_filename=kw).values_list(lev_col, flat=True)
#             print("levels in TagDictsUpl")
#             table_name = "TagDictsUpl"
#         else:
#             print("levels in TagDicts kw")
#             table_name = "TagDicts"
#     else:
#         levs = TagDicts.objects.filter(dict_filename='kelloggs_1').values_list(lev_col, flat=True)
#         print("levels in TagDicts default")
#         table_name = "TagDicts default"
#     levs = list(set(levs))
#     levs = [x for x in levs if str(x) != ' ']
#     print(levs)
#     if len(levs) == 0:
#         print("Levels for this dimension does not contain values. Using the dimension values itself")
#         if table_name == "TagDicts":
#             levs = TagDicts.objects.filter(dict_filename=kw).values_list(dim_col, flat=True)
#         elif table_name == "TagDicts default":
#             levs = TagDicts.objects.filter(dict_filename='kelloggs_1').values_list(dim_col, flat=True)
#         elif table_name == "TagDictsUpl":
#             levs = TagDictsUpl.objects.filter(dataset_filename=kw).values_list(dim_col, flat=True)
#     levs = list(set(levs))
#     levs = [x for x in levs if str(x) != ' ' and str(x) != 'nan']
#     print(levs)
#
#     # Form dataframe to hold values
#     if len(brands) > 0 and len(levs) > 0:
#         print("len(brands) > 0 and len(levs) > 0")
#         data_df = pd.DataFrame({'brand': brands})
#         # print(data_df)
#         for l in levs:
#             data_df[l] = 0
#         # print(data_df)
#
#         # Fill in values
#
#         if has_csv:
#             rids = AggTaggedData.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
#             if len(rids) == 0:
#                 rids = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
#                 print("rids in AggTaggedDataUpl")
#                 data_1 = AggTaggedDataUpl.objects.filter(dataset_filename=kw).values()
#             else:
#                 print("rids in AggTaggedData")
#                 data_1 = AggTaggedData.objects.filter(dataset_filename=kw).values()
#         else:
#             rids = AggTaggedDataRev.objects.filter(pCategory=kw).values_list('rid', flat=True)
#             print("rids in AggTaggedDataRev")
#             data_1 = AggTaggedDataRev.objects.filter(pCategory=kw).values()
#         rids = list(set(rids))
#         # print(data_1)
#
#         for r in rids:
#             # print(r)
#             tagtable_name = "None"
#             if has_csv:
#                 data2 = AggTaggedData.objects.filter(dataset_filename=kw, rid=r).values_list(brand_col, flat=True)
#
#                 if len(data2) == 0:
#                     data2 = AggTaggedDataUpl.objects.filter(dataset_filename=kw, rid=r).values_list(brand_col, flat=True)
#                     print("data2 in AggTaggedDataUpl")
#                     data2_1 = TaggedDataUpl.objects.values_list(lev_col, flat=True).filter(dataset_filename=kw, rid=r)
#                     if len(data2_1) == 0:
#                         data2_1 = TaggedDataUpl.objects.values_list(lev_col, flat=True).filter(dataset_filename=kw,
#                                                                                                rid=r)
#                     tagtable_name = "TaggedDataUpl"
#
#                 else:
#                     print("data2 in AggTaggedData")
#                     data2_1 = TaggedData.objects.values_list(lev_col, flat=True).filter(dataset_filename=kw, rid=r)
#                     if len(data2_1) == 0:
#                         data2_1 = TaggedData.objects.values_list(lev_col, flat=True).filter(dict_filename=kw, rid=r)
#                     tagtable_name = "TaggedData"
#
#             else:
#                 data2 = AggTaggedDataRev.objects.filter(pCategory=kw, rid_id=r).values_list(brand_col, flat=True)
#                 print("data2 in AggTaggedDataRev")
#                 data2_1 = TaggedDataRev.objects.values_list(lev_col, flat=True).filter(pCategory=kw, rid=r)
#                 if len(data2_1) == 0:
#                     data2_1 = TaggedDataRev.objects.values_list(lev_col, flat=True).filter(pCategory=kw,
#                                                                                            rid=r)
#                 tagtable_name = "TaggedDataRev"
#
#             data2 = list(set(list(data2)))
#             data2_1 = list(set(list(data2_1)))
#             data2_1 = [d for d in data2_1 if str(d) != ' ']
#
#             if len(data2_1) == 0:
#                 print("Levels for this dimension does not contain values. Using the dimension values itself")
#                 if tagtable_name == "TaggedData":
#                     data2_1 = TaggedData.objects.values_list(dim_col, flat=True).filter(dataset_filename=kw, rid=r)
#                     if len(data2_1) == 0:
#                         data2_1 = TaggedData.objects.values_list(dim_col, flat=True).filter(dict_filename=kw, rid=r)
#                 elif table_name == "TaggedDataUpl":
#                     data2_1 = TaggedDataUpl.objects.values_list(dim_col, flat=True).filter(dataset_filename=kw, rid=r)
#                     if len(data2_1) == 0:
#                         data2_1 = TaggedDataUpl.objects.values_list(dim_col, flat=True).filter(dataset_filename=kw,
#                                                                                                rid=r)
#                 elif table_name == "TaggedDataRev":
#                     data2_1 = TaggedDataRev.objects.values_list(dim_col, flat=True).filter(pCategory=kw, rid=r)
#                     if len(data2_1) == 0:
#                         data2_1 = TaggedDataRev.objects.values_list(dim_col, flat=True).filter(pCategory=kw,
#                                                                                                rid=r)
#             data2_1 = list(set(list(data2_1)))
#             data2_1 = [d for d in data2_1 if str(d) != ' ']
#
#             print("forming data_df")
#             # print(brands)
#             # print(levs)
#             print(data2)
#             print(data2_1)
#             for b in brands:
#                 for l in levs:
#                         if b in data2 and l in data2_1:
#                             print('%%%')
#                             data_df.ix[data_df['brand'] == b, data_df.columns.get_loc(l)] += 1
#                             print(data_df.ix[data_df['brand'] == b, data_df.columns.get_loc(l)])
#     else:
#         data_df = []
#         print("data_df not formed. returning empty data_df")
#     print(data_df)
#
#     return data_df


def getAssociationdata(kw, dim):
    # print("")
    data_df = get_assoc_values(kw, dim)
    df = data_df
    # print(df)
    if not len(df) > 0:
        print("Sorry! No records found!")
        errMsg = "It seems like no records have been tagged into any of the dimensions!"
        data_json = json.dumps(errMsg, cls=DjangoJSONEncoder)
        return data_json
    else:
        #df = pd.io.parsers.read_csv(dbConfig.dict['associationInput'])
        print("Records retrieved")
        df = df.set_index('brand')
        df1 = df
        df1 = df1.to_json(orient='index')
        # print df.describe()
        # print df.head()
        # print("-----------------------------------", df1)

        # ~~~~~~~~~~~~~~~~~~~~~~BPC
        # df.dropna(inplace=True)

        df = df.replace({0: 0.1})
        # print(df)
        try:
            ca = CA(df)

            fig = plt.figure('Brand Perception Chart')
            # ######################### Comment out to display only Radar chart
            #ca.plot()
            #    plt.figure(101)
            # ca.scree_diagram()

            # plt.show()
            # #########################
            b = mpld3.fig_to_dict(fig)

            dict_combine = {"source_data": df1, "graph_data": b}
            # data1 = serializers.serialize("json", dict_combine)

            data_json = json.dumps(dict_combine, cls=DjangoJSONEncoder)
            # print("-------------------------------------------------------------------------------")
            # print("Data_json is : neo -- ", data_json)
            # print(type(data_json))
            print("returning from getassocdata with df")
            return data_json

        except:
            print("returning from getassocdata with empty df")
            return []
        # ~~~~~~~~~~~~~~~~~~~~~~~~


def getTopposnegOverall(kw):
    kw = str(kw)[:len(kw) - 4]

    test = Uploads.objects.filter(pCategory=kw).values()
    if test:
        top_pos_ids = UploadAnalyses.objects.filter(rid__pCategory=kw, sentiment='Positive').order_by('-sentiScore') \
                .values_list('rid_id', flat=True)[:2]
        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        top_neg_ids = UploadAnalyses.objects.filter(rid__pCategory=kw, sentiment='Negative').order_by('sentiScore') \
                       .values_list('rid_id', flat=True)[:2]
        top_neg_ids1 = list(top_neg_ids)
        #print(top_neg_ids1)

        pos_data = Uploads.objects.filter(rid__in=top_pos_ids1).only('rTitle','rText')
        #print(pos_data)

        neg_data = Uploads.objects.filter(rid__in=top_neg_ids1).only('rTitle','rText')
        #print(neg_data)

        #data = pos_data.union(neg_data)
        data = pos_data | neg_data
        # print("Printing data")
        #print(data)

        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json

    else:
        top_pos_ids = SocialAnalyses.objects.filter(aid__dataset_filename=kw, sentiment='Positive').order_by('-sentiScore') \
                          .values_list('aid_id', flat=True)[:2]

        top_pos_ids1 = list(top_pos_ids)
        #print(top_pos_ids1)

        top_neg_ids = SocialAnalyses.objects.filter(aid__dataset_filename=kw, sentiment='Negative').order_by('sentiScore') \
                       .values_list('aid_id', flat=True)[:2]
        top_neg_ids1 = list(top_neg_ids)
        #print(top_neg_ids1)

        pos_data = Social.objects.filter(aid__in=top_pos_ids1).only('rTitle', 'rText')
        #print(pos_data)

        neg_data = Social.objects.filter(aid__in=top_neg_ids1).only('rTitle','rText')
        #print(neg_data)

        #data = pos_data.union(neg_data)
        data = pos_data | neg_data
        #print("Printing data")
        #print(data)

        data1 = serializers.serialize("json", data)
        data_json = json.dumps(data1, cls=DjangoJSONEncoder)
        return data_json


def getBrand(kw):
    brands = Product.objects.filter(pCategory=kw).distinct().values('pBrand')  # to return dictionary of values for each column
    #brands = Product.objects.filter(pCategory=request).distinct().values_list('pBrand', flat=True)  # to return only values of that column
    brands_json = json.dumps(list(brands), cls=DjangoJSONEncoder)
    return brands_json


def getSource(kw, brand):
    sources = Product.objects.filter(pCategory=kw, pBrand__in=brand).distinct().values_list('siteCode', flat=True)  # to return dictionary of values for each column
    #print(sources)
    #sources = Product.objects.filter(pCategory=kw, pBrand__in=brand).distinct().values('siteCode')  # to return dictionary of values for each column
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    sources1 = []
    for s in list(sources):
        for i, r in sources_file.iterrows():
            if s == r['siteCode']:
                sources1.append(r['siteName'])
    #print(sources1)
    sources_json = json.dumps(sources1, cls=DjangoJSONEncoder)
    #print sources_json
    return sources_json


def getSourceRevmap1(source_vals):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    sources1 = []

    for s in list(source_vals):
        sources1.append([r['siteCode'] for i, r in sources_file.iterrows() if s == r['siteName']])
    #print(sources1)
    sources_json = json.dumps(list(sources1), cls=DjangoJSONEncoder)
    #print sources_json
    return sources_json


def getSku(kw, brand, source):
    # print("value of source in getsku:", source)
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)

    sku = Product.objects.filter(pCategory=kw, pBrand__in=brand, siteCode__in=source1).distinct().values('pModel')  # to return dictionary of values for each column
    sku_json = json.dumps(list(sku), cls=DjangoJSONEncoder)
    return sku_json


def getChart1(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    dates = Review.objects.values_list('rDate')
    dates2 = Review.objects.values_list('rDate2')
    data = dates.annotate(Count('rid')).filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source
                                               , pid__pModel__in=sku).order_by('rDate')
    if (fromDate == "" or toDate == ""):
        data2 = dates2.annotate(Count('rid')).filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source
                                                   , pid__pModel__in=sku).order_by('rDate2')
    else:
        data2 = dates2.annotate(Count('rid')).filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source
                                                    , pid__pModel__in=sku, rDate2__range=[fromDate, toDate]).order_by('rDate2')

    d2 = list(data2)
    a = list(data)
    # print(a)
    # print(d2)
    c = [[int(time.mktime(b[0].timetuple()))*1000, b[1]] for b in d2]
    #print("--------------------------------------------------------------")
    #print(dir(data))
    #print(c)
    #print("--------------------------------------------------------------")
    #print("Query= ", data.query)
    data_json = json.dumps(c, cls=DjangoJSONEncoder)
    #print(data_json)
    return data_json


def getCommonReviewCountChart(kw):  # chart1
    print("Inside getCommonReviewCount")
    kw = str(kw)[:len(kw) - 4]

    test = Uploads.objects.filter(pCategory=kw).values()
    if test:
        # CODE FOR REVIEW UPLOADS EXCLUSIVELY ############################################
        data1 = Uploads.objects.filter(pCategory=kw).values_list('rid')

        dates = Uploads.objects.filter(pCategory=kw).values_list('rDate')
        dates2 = Uploads.objects.filter(pCategory=kw).values_list('rDate2')

        data = dates.annotate(Count('rid')).filter(rid__in=data1).order_by('rDate')
        #print(data)

        a = list(data)

        c = [[int(time.mktime(b[0].timetuple()))*1000, b[1]] for b in a]
        #print("--------------------------------------------------------------")
        #print(dir(data))
        #print(c)
        #print("--------------------------------------------------------------")
        #print("Query= ", data.query)
        data_json = json.dumps(c, cls=DjangoJSONEncoder)
        return data_json
        #################################################################################
    else:
        data1 = Social.objects.filter(dataset_filename=kw).values_list('rid')

        dates = Social.objects.filter(dataset_filename=kw).values_list('rDate')
        dates2 = Social.objects.filter(dataset_filename=kw).values_list('rDate2')

        data = dates.annotate(Count('rid')).filter(rid__in=data1).order_by('rDate')
        #print(data)

        a = list(data)

        c = [[int(time.mktime(b[0].timetuple())) * 1000, b[1]] for b in a]

        data_json = json.dumps(c, cls=DjangoJSONEncoder)
        #print(data_json)
        return data_json



def neighborhood(iterable):
    iterator = iter(iterable)
    prev_item = None
    current_item = next(iterator)  # throws StopIteration if empty.
    for next_item in iterator:
        yield (prev_item, current_item, next_item)
        prev_item = current_item
        current_item = next_item
    yield (prev_item, current_item, None)


def getChart2(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    if (fromDate == "" or toDate == ""):
        data2 = Review.objects.filter\
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku)\
            .values_list('pid__pBrand', 'pid__pModel')\
            .annotate(average_rating=Avg('pid__pRating'))
        data1 = Review.objects.filter\
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku).values_list('pid__pBrand')\
            .annotate(average_rating=Avg('pid__pRating'))
    else:
        data2 = Review.objects.filter\
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku, rDate2__range=[fromDate, toDate])\
            .values_list('pid__pBrand','pid__pModel')\
            .annotate(average_rating=Avg('pid__pRating'))
        data1 = Review.objects.filter\
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku, rDate2__range=[fromDate, toDate])\
            .values_list('pid__pBrand')\
            .annotate(average_rating=Avg('pid__pRating'))

    a = list(data1)
    b = list(data2)
    #print("--------------------------------------------------------------")
    #print("--------------------------------------------------------------")
    #print("Query= ", data2.query)
    dict1 = {}
    response1 = []
    #print(data_json1)
    #print("--------------------------------------------------------------")
    #a
    # [["Element", 4.0], ["Samsung", 1.0], ["Sceptre", 4.03975], ["Seiki", 3.0], ["TCL", 4.33846], ["VIZIO", 4.5]]
    #b
    # [["Element", "B01HQS8UZA", 4.0], ["Samsung", "301688015", 1.0], ["Sceptre", "27678567", 4.0],
    #  ["Sceptre", "55042148", 4.5], ["Sceptre", "55427159", 3.5], ["Sceptre", "B00W2T70IM", 4.2],
    #  ["Seiki", "55277725", 3.0], ["TCL", "B01MTGM5I9", 4.8], ["TCL", "B01MU1GBLL", 4.2], ["VIZIO", "49228250", 4.5]]
    for i in a:
        dict1["name"] = i[0]
        dict1["y"] = i[1]
        dict1["drilldown"] = i[0]
        response1.append(dict1)
        dict1 = {}

    series = []
    temp_list = []
    temp1 = []
    dict2 = {}

    for prev, item, next in neighborhood(b):
        if next is not None:
            if item[0] == next[0]:
                temp_list.append(item[1])
                temp_list.append(item[2])
                temp1.append(temp_list)
                temp_list = []
                continue
            else:
                temp_list.append(item[1])
                temp_list.append(item[2])
                temp1.append(temp_list)
        else:
            temp_list.append(item[1])
            temp_list.append(item[2])
            temp1.append(temp_list)

        dict2["name"] = item[0]
        dict2["id"] = item[0]
        dict2["data"] = temp1
        series.append(dict2)
        dict2 = {}
        temp1 = []
        temp_list = []

    dict2['series'] = series
    response = {}
    response['response1'] = response1
    response['dict2'] = dict2
    #print response
    response_json = json.dumps(response, cls=DjangoJSONEncoder)
    return response_json


def getChart3(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    dates = Review.objects.values_list('rDate')
    dates2 = Review.objects.values_list('rDate2')

    if (fromDate == "" or toDate == ""):
        data2 = Review.objects.filter \
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku) \
            .values_list('pid__pBrand', 'pid__pModel') \
            .annotate(Count('pid__pModel'))
    else:
        data2 = Review.objects.filter \
            (pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku, rDate2__range=[fromDate, toDate]) \
            .values_list('pid__pBrand', 'pid__pModel') \
            .annotate(Count('pid__pModel'))

    #print (brand)
    d2 = list(data2)
    series = []
    temp_list = []
    temp1 = []
    dict2 = {}
    temp_dict = {}
    temp_dict1 = {}
    for prev, item, next in neighborhood(d2):
        if next is not None:
            if item[0] == next[0]:
                temp_dict[item[1]] = item[2]
            else:
                temp_dict[item[1]] = item[2]
                temp_dict1[item[0]] = temp_dict
                temp_dict = {}
        else:
            if item[0] == prev[0]:
                temp_dict[item[1]] = item[2]
                temp_dict1[item[0]] = temp_dict
            else:
                temp_dict = {}
                temp_dict[item[1]] = item[2]
                temp_dict1[item[0]] = temp_dict


    #print(temp_dict1)
    #a = list(data)
    dict1 = {}
    # for i in d2:
    #     dict
    #print(a)
    #print(d2)
    #c = [[int(time.mktime(b[0].timetuple()))*1000, b[1]] for b in d2]
    #print("--------------------------------------------------------------")
    #print(dir(data))
    #print(c)
    # print("--------------------------------------------------------------")
    #print("Query= ", data.query)
    data_json = json.dumps(temp_dict1, cls=DjangoJSONEncoder)
    #print(data_json)
    return data_json


def getPieChart(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    #print(source1)
    source = source1

    if fromDate=="" and toDate == "":
        data2 = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source,
                                      pid__pModel__in=sku) \
            .values_list('pid__siteCode') \
            .annotate(siteCode_count=Count('rid'))
    else:
        data2 = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source,
                                      pid__pModel__in=sku, rDate2__range=[fromDate, toDate]) \
            .values_list('pid__siteCode') \
            .annotate(siteCode_count=Count('rid'))
    # print("Printing data2 for piechart")
    #print(data2)
    dict_list = []
    one_dict = {}
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)

    for d in data2:
        one_dict['name'] = [r['siteName'] for i, r in sources_file.iterrows() if d[0] == r['siteCode']]
        #print(one_dict['name'])
        one_dict['y'] = d[1]
        dict_list.append(one_dict.copy())
    #print dict_list
    data_json = json.dumps(dict_list, cls=DjangoJSONEncoder)
    return data_json


def getCategChartRev(kw, brand, source, sku, fromDate, toDate):
    sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
    source1 = []
    for s in list(source):
        for i, r in sources_file.iterrows():
            if s == r['siteName']:
                source1.append(r['siteCode'])
    source = source1

    series_data = []  # append this dict to a list later
    # skeleton for series_data:
    # [{name:__,y:__,drilldown:__ } ]

    drilldown_series_data = []
    # skeleton for drilldown_series_data:
    # { series: [
    #     { name:__, id:__, data: [
    #                       { name:__, y:__, drilldown:__},
    #                       { name:__,id:__, data:[
    #                                         [__,__],[__,__]
    #                                       ]
    #                       }
    #                     ]
    #     }
    #    ]
    # }


    try:
        if fromDate == "" and toDate == "":
            rev_ids = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source, pid__pModel__in=sku).values_list('rid', flat=True)
            cat_pri_qs = ContentCategoryRev.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(cat_count=Count('category_pri'))
            # print("cat_pri_qs", cat_pri_qs)

        else:
            rev_ids = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source,pid__pModel__in=sku, rDate2__range=[fromDate,toDate]).values_list('rid', flat=True)
            cat_pri_qs = ContentCategoryRev.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(cat_count=Count('category_pri'))
            # print("cat_pri_qs",cat_pri_qs)
            #cat_pri = list(set(ContentCategoryRev.objects.filter(rid_id__in=rev_ids).values_list('category_pri',flat=True)))

        # print("cat_pri_qs", cat_pri_qs)
        # print("cat_sec_qs", cat_sec_qs)

        series_data_dict = {}

        cat_pri_count_total = sum([c['cat_count'] for c in cat_pri_qs])
        # print("cat_pri_count_total",cat_pri_count_total)
        # To populate series []
        for p in cat_pri_qs:
            print("inside 1st loop")
            series_data_dict["name"] = p['category_pri']
            series_data_dict["y"] = float(p['cat_count'])/float(cat_pri_count_total) * 100
            print(p['cat_count'],cat_pri_count_total)
            series_data_dict["drilldown"] = str(p['category_pri']).split('/')[1].lower()
            series_data.append(series_data_dict.copy())

        # To populate drilldown {} - first drilldown
        for p in cat_pri_qs:
            print("inside 2nd loop")
            drilldown_series_dict = dict()
            drilldown_series_dict["name"] = p['category_pri']
            drilldown_series_dict["id"] = str(p['category_pri']).split('/')[1].lower()
            drilldown_series_dict["data"] = []

            cat_sec_qs = ContentCategoryRev.objects.filter(category_pri=p['category_pri'],rid_id__in=rev_ids).values('category_sec').annotate(cat_count=Count('category_sec'))
            for s in cat_sec_qs:
                #  To add second-level drilldown ###
                drilldown_series_dict_data = dict()
                if len(str(s['category_sec']).split('/')) == 3:
                    drilldown_series_dict_data["name"] = "/" + str(s['category_sec']).split('/')[2]
                    drilldown_series_dict_data["y"] = float(s['cat_count']) / float(p['cat_count']) * 100
                    drilldown_series_dict_data["drilldown"] = drilldown_series_dict["id"] + '-' + str(s['category_sec']).split('/')[2].lower()

                    # drilldown_series_dict["data"].append(drilldown_series_dict_data.copy())
                else:
                    drilldown_series_dict_data["name"] = "/Others"
                    drilldown_series_dict_data["y"] = float(s['cat_count']) / float(p['cat_count']) * 100
                    drilldown_series_dict_data["drilldown"] = None

                drilldown_series_dict["data"].append(drilldown_series_dict_data.copy())

            drilldown_series_data.append(drilldown_series_dict.copy())

        # To populate drilldown {} - second drilldown
        for p in cat_pri_qs:
            print("inside 3rd loop")
            cat_sec_qs = ContentCategoryRev.objects.filter(category_pri=p['category_pri'],rid_id__in=rev_ids).values('category_sec').annotate(
                cat_count=Count('category_sec'))
            for s in cat_sec_qs:
                drilldown_series_dict = dict()
                if len(str(s['category_sec']).split('/')) == 3:
                    drilldown_series_dict["name"] = s['category_sec']
                    drilldown_series_dict["id"] = str(p['category_pri']).split('/')[1].lower() + '-' + str(s['category_sec']).split('/')[2].lower()
                    drilldown_series_dict["data"] = []

                    cat_ter_qs = ContentCategoryRev.objects.filter(category_pri=p['category_pri'],category_sec=s['category_sec'],
                                                                   rid_id__in=rev_ids).values('category_ter').annotate(
                                                                   cat_count=Count('category_ter'))
                    if len(cat_ter_qs) > 0:
                        for t in cat_ter_qs:
                            if len(str(t['category_ter']).split('/')) == 4:
                                drilldown_series_dict['data'].append(['/' + str(t['category_ter']).split('/')[3], float(t['cat_count'])/float(s['cat_count'])*100])
                            else:
                                drilldown_series_dict['data'].append(['/Others', float(t['cat_count']) / float(s['cat_count']) * 100])
                    else:
                        drilldown_series_dict['data'].append(['/Others', 100])

                    drilldown_series_data.append(drilldown_series_dict.copy())
    except:
        print("Error while forming data for Category pie chart")
        print(traceback.print_exc())
    # df = pd.DataFrame()
    # df['pCategory'] = kw
    # df['series_data'] = series_data
    # df['drilldown_series_data'] = drilldown_series_data
    #
    # df.to_csv(dbConfig.dict['dbfolderPath'] + "_" + kw.replace(" ", "-") + ".csv", header=True, index=False)
    # print("series_data", series_data)
    print("drilldown series data", drilldown_series_data)
    return json.dumps([series_data, drilldown_series_data])


def getCategChart(kw):
    if '.csv' in kw:
        kw = kw[0:len(kw) - 4]

    series_data = []  # append this dict to a list later
    # skeleton for series_data:
    # [{name:__,y:__,drilldown:__ } ]

    drilldown_series_data = []
    # skeleton for drilldown_series_data:
    # { series: [
    #     { name:__, id:__, data: [
    #                       { name:__, y:__, drilldown:__},
    #                       { name:__,id:__, data:[
    #                                         [__,__],[__,__]
    #                                       ]
    #                       }
    #                     ]
    #     }
    #    ]
    # }

    tabl_name = "Upl"
    rev_ids = Uploads.objects.filter(pCategory=kw).values_list('rid', flat=True)
    if len(rev_ids) == 0:
        rev_ids = Social.objects.filter(dataset_filename=kw).values_list('rid', flat=True)
        tabl_name = "Soc"
        cat_pri_qs = ContentCategoryUpl.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(
            cat_count=Count('category_pri'))
    else:
        tabl_name = "Upl"
        cat_pri_qs = ContentCategorySoc.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(cat_count=Count('category_pri'))


    # print("cat_pri_qs", cat_pri_qs)
    # print("cat_sec_qs", cat_sec_qs)

    series_data_dict = {}

    cat_pri_count_total = sum([c['cat_count'] for c in cat_pri_qs])
    # print("cat_pri_count_total",cat_pri_count_total)
    # To populate series []
    for p in cat_pri_qs:
        series_data_dict["name"] = p['category_pri']
        series_data_dict["y"] = float(p['cat_count'])/float(cat_pri_count_total) * 100
        print(p['cat_count'],cat_pri_count_total)
        series_data_dict["drilldown"] = str(p['category_pri']).split('/')[1].lower()
        series_data.append(series_data_dict.copy())

    # To populate drilldown {} - first drilldown
    for p in cat_pri_qs:
        drilldown_series_dict = dict()
        drilldown_series_dict["name"] = p['category_pri']
        drilldown_series_dict["id"] = str(p['category_pri']).split('/')[1].lower()
        drilldown_series_dict["data"] = []

        if tabl_name == "Upl":
            cat_sec_qs = ContentCategoryUpl.objects.filter(category_pri=p['category_pri'],rid_id__in=rev_ids).values('category_sec').annotate(cat_count=Count('category_sec'))
        else:
            cat_sec_qs = ContentCategorySoc.objects.filter(category_pri=p['category_pri'], rid_id__in=rev_ids).values(
                'category_sec').annotate(cat_count=Count('category_sec'))
        for s in cat_sec_qs:
            #  To add second-level drilldown ###
            drilldown_series_dict_data = dict()
            if len(str(s['category_sec']).split('/')) == 3:
                drilldown_series_dict_data["name"] = "/" + str(s['category_sec']).split('/')[2]
                drilldown_series_dict_data["y"] = float(s['cat_count']) / float(p['cat_count']) * 100
                drilldown_series_dict_data["drilldown"] = drilldown_series_dict["id"] + '-' + str(s['category_sec']).split('/')[2].lower()

                # drilldown_series_dict["data"].append(drilldown_series_dict_data.copy())
            else:
                drilldown_series_dict_data["name"] = "/Others"
                drilldown_series_dict_data["y"] = float(s['cat_count']) / float(p['cat_count']) * 100
                drilldown_series_dict_data["drilldown"] = None

            drilldown_series_dict["data"].append(drilldown_series_dict_data.copy())

        drilldown_series_data.append(drilldown_series_dict.copy())

    # To populate drilldown {} - second drilldown
    for p in cat_pri_qs:
        if tabl_name == "Upl":
            cat_sec_qs = ContentCategoryUpl.objects.filter(category_pri=p['category_pri'],rid_id__in=rev_ids).values('category_sec').annotate(
            cat_count=Count('category_sec'))
        else:
            cat_sec_qs = ContentCategorySoc.objects.filter(category_pri=p['category_pri'], rid_id__in=rev_ids).values(
                'category_sec').annotate(cat_count=Count('category_sec'))

        for s in cat_sec_qs:
            drilldown_series_dict = dict()
            if len(str(s['category_sec']).split('/')) == 3:
                drilldown_series_dict["name"] = s['category_sec']
                drilldown_series_dict["id"] = str(p['category_pri']).split('/')[1].lower() + '-' + str(s['category_sec']).split('/')[2].lower()
                drilldown_series_dict["data"] = []

                cat_ter_qs = ContentCategoryRev.objects.filter(category_pri=p['category_pri'],category_sec=s['category_sec'],
                                                               rid_id__in=rev_ids).values('category_ter').annotate(
                                                               cat_count=Count('category_ter'))
                if len(cat_ter_qs) > 0:
                    for t in cat_ter_qs:
                        if len(str(t['category_ter']).split('/')) == 4:
                            drilldown_series_dict['data'].append(['/' + str(t['category_ter']).split('/')[3], float(t['cat_count'])/float(s['cat_count'])*100])
                        else:
                            drilldown_series_dict['data'].append(['/Others', float(t['cat_count']) / float(s['cat_count']) * 100])
                else:
                    drilldown_series_dict['data'].append(['/Others', 100])

                drilldown_series_data.append(drilldown_series_dict.copy())

    # print("series_data", series_data)

    # print("drilldown series data", drilldown_series_data)

    return json.dumps([series_data, drilldown_series_data])


def getWordCloudRev(kw, brand, source, sku, fromDate, toDate):
    wc_chartdata = []
    resp = []
    try:
        sources_file = pd.read_csv(dbConfig.dict['sourcesUrl'], header=0)
        source1 = []
        for s in list(source):
            for i, r in sources_file.iterrows():
                if s == r['siteName']:
                    source1.append(r['siteCode'])
        source = source1

        if fromDate == "" and toDate == "":
            rev_ids = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source,
                                            pid__pModel__in=sku).values_list('rid', flat=True)
            wc_chartdata = ContentCategoryRev.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(
                cat_count=Count('category_pri'))

        else:
            rev_ids = Review.objects.filter(pid__pCategory=kw, pid__pBrand__in=brand, pid__siteCode__in=source,
                                            pid__pModel__in=sku, rDate2__range=[fromDate, toDate]).values_list('rid',
                                                                                                               flat=True)
            wc_chartdata = ContentCategoryRev.objects.filter(rid_id__in=rev_ids).values('category_pri').annotate(
                cat_count=Count('category_pri'))

        for w in wc_chartdata:
            resp_dict = {"name": "", "weight": 0}
            resp_dict["name"] = w['category_pri']
            resp_dict["weight"] = w['cat_count']

            resp.append(resp_dict.copy())

        print("resp=",resp)
    except:
        print("Error while getting wordcloud data")
        print(traceback.print_exc())
    return json.dumps(resp)


def getWordCloud(kw):

    return