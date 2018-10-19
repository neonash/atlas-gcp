import pandas as pd
from atlas.models import Review, Uploads, DimenMapUpl, DimenMap, Social, ContentCategoryRev, ContentCategoryUpl, ContentCategorySoc
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import os
from django.http import HttpResponse
import re
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import traceback
from atlas.config import dbConfig

reload(sys)
sys.setdefaultencoding('utf8')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dbConfig.dict['gcp_servicekey_path']

status = 200


def clean_rev(curr_rev):
    curr_rev = curr_rev.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    curr_rev = curr_rev.replace("&nbsp;", " ").replace("&gt;", " ").replace("&lt;", " ").replace("&quot;", " ")
    curr_rev = curr_rev.replace(" & ", " and ").replace("-", " ")
    curr_rev = re.sub(r'[^\w\s]*', "", curr_rev)  # 0 or more non-(alphanumeric or whitespace)
    curr_rev = curr_rev.strip()
    curr_rev = re.sub(r'\s{2,}', ' ', curr_rev)

    return curr_rev


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def classify_text(tabl_name, id, text):
    try:
        """Classifies content categories of the provided text."""
        client = language.LanguageServiceClient()
        term = text
        stop_words = set(stopwords.words('english'))
        # print(stop_words)
        word_tokens = word_tokenize(text)
        # print(word_tokens)
        filtered_sentence_list = list(set([w for w in word_tokens if not w.lower() in stop_words]))

        # print(filtered_sentence_list)
        # print(len(filtered_sentence_list))
        if len(filtered_sentence_list) > 0:
            while len(filtered_sentence_list) < 20:
                # filtered_sentence_list = filtered_sentence_list.extend(filtered_sentence_list)
                filtered_sentence_list *= 2

        # print(filtered_sentence_list)
        # How many elements each
        # list should have
        n = 10

        x = list(divide_chunks(filtered_sentence_list, n))
        # print ("x = ", x)
        full_cat_name_list = []
        full_confidence_list = []
        term_list = []
        #output = pd.DataFrame()
        for x1 in x:
            temp_x1 = []
            if len(x1) < 10:
                while len(temp_x1) < 20:
                    temp_x1.extend(x1)
            else:
                temp_x1.extend(x1 + x1)
            # print(temp_x1)
            filtered_sentence_str = ' '.join(temp_x1)

            print("tokenised text ", filtered_sentence_str)
            # print(len(filtered_sentence_str))

            if isinstance(filtered_sentence_str, six.binary_type):
                filtered_sentence_str = filtered_sentence_str.decode('utf-8')
            document = types.Document(
                content=filtered_sentence_str.encode('utf-8'),
                type=enums.Document.Type.PLAIN_TEXT)
            # print(document)
            categories = client.classify_text(document).categories
            # print("categories=", categories)

            if len(categories) > 0:

                for categ in categories:
                    # output['term'] = term_list
                    print(u'{:<16}: {}'.format('name', categ.name))
                    categ_pri = '/' + str(categ.name).split('/')[1]
                    categ_sec = ""
                    categ_ter = ""
                    if len(str(categ.name).split('/')) == 4:
                        categ_sec = str(categ.name).rsplit('/', 1)[0]
                        categ_ter = categ.name
                    elif len(str(categ.name).split('/')) == 3:
                        categ_ter = ""
                        categ_sec = categ.name


                    # cat_name_list = []
                    # cat_name_list.append(category.name)
                    if not categ.name in full_cat_name_list:
                        # term_list = []
                        term_list.append(term)
                        full_cat_name_list.append(categ.name)
                        full_confidence_list.append(categ.confidence)

                        if tabl_name == "Review":
                            ccr_obj = ContentCategoryRev.objects.create(rid_id=id,category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,confidence=categ.confidence).save()
                        elif tabl_name == "Uploads":
                            ccr_obj = ContentCategoryUpl.objects.create(rid_id=id,category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,
                                                                        confidence=categ.confidence).save()
                        elif tabl_name == "Social":
                            ccr_obj = ContentCategorySoc.objects.create(rid_id=id, category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,
                                                                        confidence=categ.confidence).save()

                    else:
                        if full_confidence_list[full_cat_name_list.index(
                                categ.name)] < categ.confidence:  # if new confidence is more than old confidence
                            full_confidence_list[full_cat_name_list.index(categ.name)] = categ.confidence
                            if tabl_name == "Review":
                                ccr_obj = ContentCategoryRev.objects.get(rid_id=id, category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,)
                                ccr_obj.confidence = categ.confidence
                                ccr_obj.save()
                            elif tabl_name == "Uploads":
                                ccr_obj = ContentCategoryUpl.objects.create(rid_id=id, category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,)
                                ccr_obj.confidence = categ.confidence
                                ccr_obj.save()
                            elif tabl_name == "Social":
                                ccr_obj = ContentCategorySoc.objects.create(rid_id=id, category_pri=categ_pri,category_sec=categ_sec,category_ter=categ_ter,)
                                ccr_obj.confidence = categ.confidence
                                ccr_obj.save()

                    # output['category'] = cat_name_list
                    print(u'{:<16}: {}'.format('confidence', categ.confidence))
                    # confidence_list = []
                    # confidence_list.append(category.confidence)
                    # output['confidence'] = confidence_list
                    print(u'=' * 20)
        # print("full_cat_name_list ", full_cat_name_list)
        # print("full_confidence_list", full_confidence_list)

        # output = pd.DataFrame()
        # output['rText'] = term_list
        # output['category'] = full_cat_name_list
        # output['confidence'] = full_confidence_list

        # with open(r"C:\\Users\\akshat.gupta\\Desktop\\google_content_categories_output-rev.csv", 'w') as f:
        #     output.to_csv(f, header=True, index=False, encoding='utf-8')
        #    # cat_dict = dict(zip(full_cat_name_list, full_confidence_list))
    except:
        print(traceback.print_exc())


def main(request):
    try:
        print("classifying data for ", request)
        query1 = request
        has_csv = False
        if ".csv" in query1:
            has_csv = True
            query1 = query1[:len(query1) - 4]

        #df = pd.read_csv("C:\\Users\\akshat.gupta\\Desktop\\Book2.csv", encoding='iso-8859-1')
        tabl_name = ""
        if not has_csv:
            rev_qs = Review.objects.filter(pid_id__pCategory=query1).values()
            tabl_name = "Review"
        else:
            rev_qs = Uploads.objects.filter(pCategory=query1).values('rid')
            if len(rev_qs) == 0:
                rev_qs = Social.objects.filter(dataset_filename=query1).values('rid')
                tabl_name = "Social"
            else:
                tabl_name = "Uploads"
        print("data in table ", tabl_name)
        for r in rev_qs:
            i = 0
            if len(r['rText']) > 0:
                # print(m)
                classify_text(tabl_name, r['rid'], r['rText'])
            else:
                i += 1  # to execute only 1st time

        print("Content categories Done")
        status = 200
    except:
        print("Error while classifying content categories!")
        print(traceback.print_exc())
        status = 500
    return [status]
