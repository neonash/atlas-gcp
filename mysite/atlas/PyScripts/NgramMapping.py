import pandas as pd
from atlas.models import Product, Review, Analysis, TaggedDataRev, Uploads, DimenMapUpl, TagDictsUpl, TaggedDataUpl, DimenMap, Social, TaggedData, AggTaggedData, AggTaggedDataRev, AggTaggedDataUpl
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import ATLAS1
import traceback
import re
import itertools
from collections import OrderedDict


def clean_text(curr_rev):
    curr_rev = str(curr_rev)
    curr_rev = curr_rev.replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("#", "")  # for escape characters and hashtags
    curr_rev = curr_rev.lower().replace("retweeted", "").replace("retweet", "")
    curr_rev = re.sub(r'^@[\w]*', "", curr_rev)  # for removing "@<username>"
    curr_rev = curr_rev.replace("&nbsp;", " ").replace("&gt;", " ").replace("&lt;", " ").replace("&quot;", " ")  # for html characters
    curr_rev = curr_rev.replace(" & ", " and ").replace("-", " ")
    curr_rev = re.sub(r'[^\w\s]*', "", curr_rev)  # 0 or more non-(alphanumeric or whitespace)
    curr_rev = curr_rev.strip()
    curr_rev = re.sub(r'\s{2,}', ' ', curr_rev)  # for additional whitespaces
    return curr_rev


def clean_ngram(ng):
    # print(re.sub(r'\'\w', "", ng))
    ng = re.sub("\'\w", "", ng)
    if len(ng) > 5:
        ng = ng[:len(ng) - 1]  # removes 2 characters from end of str
    elif len(ng) > 3:
        ng = ng[:len(ng)]  # removes 1 character from end of str

    return ng


def aggregate(tagged_df, request):
    rids_list = tagged_df.rid.unique()
    # print(rids_list)
    dims_list = list()
    excl_dims_list = list()
    # dims_list = [d for d in tagged_df.columns.values.tolist() if d not in ['ngram', 'rid', 'aid'] and "_" not in d]
    for d in tagged_df.columns.values.tolist():
        if d not in ['ngram', 'rid', 'aid'] and "_" not in d:
            dims_list.append(d)
        elif d in ['rid', 'aid'] and "_" not in d:
            excl_dims_list.append(d)
    # print dims_list
    # print excl_dims_list
    final_cols = list()
    final_cols.extend(excl_dims_list)
    final_cols.extend(dims_list)
    # print(final_cols)
    agg_df = pd.DataFrame(columns=final_cols)
    try:
        for r in rids_list:
            df_by_rid = tagged_df.loc[tagged_df['rid'] == r]
            # print df_by_rid

            dict1 = OrderedDict((d, "") for d in dims_list)

            for d in dims_list:
                # print d
                dict1[d] = df_by_rid[d].unique().tolist()
                # dict1[d] = [d1 for d1 in dict1[d] if not str(d1) == 'nan']
                dict1[d] = [d1 for d1 in dict1[d]]
            # print dict1

            big_list = []
            for l in dict1.values():
                big_list.append(l)
            # print big_list
            cross_product = list(itertools.product(*big_list))

            count_check = [len(cross_product[c]) for c in range(len(cross_product))]

            for c in range(len(cross_product)):
                str_list = [str(c1).lower() for c1 in list(cross_product[c])]
                # print(str_list)
                count_check[c] = str_list.count("nan")
            # print(count_check)

            fin_idx = [i for i in range(len(count_check)) if count_check[i] == min(count_check)]
            # print(fin_idx)
            try:
                for f in fin_idx:
                    le = list()
                    le.append(str(r))
                    le.extend(list(cross_product[f]))

                    le1 = list()
                    le1.append(le)

                    le_df = pd.DataFrame(le1, columns=final_cols)
                    agg_df = agg_df.append(le_df)

            except Exception as e:
                print("Inside exception1:")
                print e.message, e.args
            print("***")
    except Exception as e:
        print ("Inside Exception 2")
        print e.message, e.args
    print("Outta the loop")
    # print(agg_df)
    return agg_df


def main(request, dictfile):
    statuscode = 500
    print(dictfile)

    # source_df= pd.read_csv(sourcefile, dtype={'ARTICLE_ID': str})

    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    source_qs = Review.objects.filter(rid__startswith=request).values()

    # print("source qs akshat", source_qs)
    source_df = pd.DataFrame.from_records(source_qs)

    # print("source df akshat", source_df)

    # source_df['rid'] = source_df['rid'].apply(lambda x: '%.0f' % x)  # formats the column to float
    source_df['rid'] = source_df['rid'].astype('str')  # formats the column to str
    print("source df id", source_df['rid'])

    dict_df = pd.read_csv(dictfile, encoding='utf-8')

    tagged_df_cols = ['rid']
    #print(tagged_df_cols)
    tagged_df_cols.extend(dict_df.columns)
    tagged_df = pd.DataFrame(columns=tagged_df_cols)

    # tagged_df['ARTICLE_ID'] = pd.to_numeric(tagged_df['ARTICLE_ID'], errors='coerce')
    # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype('float64)
    agg_df = None
    try:
        for s in source_qs:

            curr_conv = s['rText']
            curr_conv = clean_text(curr_conv)

            for i2, r2 in dict_df.iterrows():
                curr_entry = []
                # str_to_match = str(r2['ngram']).center(len(r2['ngram']) + 2, ' ')
                ng_to_match = str(r2['ngram'])
                ng_to_match = clean_ngram(ng_to_match)
                try:
                    # if str_to_match[:len(str_to_match)-2].lower() in curr_conv.lower():   # adds leading and trailing whitespaces to match as one phrase
                    mat = re.findall(ng_to_match.lower(), curr_conv.lower(), re.I)
                    if len(mat) > 0:
                        # print(ng_to_match, curr_conv)
                        #print(r1['ARTICLE_ID'])

                        curr_entry.append(str(s['rid']))
                        curr_entry.extend(r2.tolist())  # condition, slicing
                        # print(curr_entry)
                        tagged_df.loc[len(tagged_df)] = curr_entry
                except TypeError:
                    pass

        # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype(float)
        # df1 = df.apply(pd.to_numeric, args=('coerce',))

        print("tagged_df", tagged_df)

        # Insert tagged data into database #############################################
        dict_name = ""
        if "electronics" in str(dictfile).lower():
            dict_name = 'speakers_1'
        elif "supplements" in str(dictfile).lower():
            dict_name = 'RB'
        elif "dimensions" in str(dictfile).lower():
            dict_name = 'kelloggs_1'
        print(dict_name)
        try:
            rs = DimenMap.objects.values().get(dict_filename=dict_name)
        except:
            rs = DimenMap.objects.filter(dict_filename=dict_name).values()[0:1]
            rs = rs[0]

        headers_list = [t for t in tagged_df_cols if t not in ['rid', 'ngram']]
        print(headers_list)
        try:
            for idx, row in tagged_df.iterrows():
                # dict2 = OrderedDict((el, " ") for el in rs.keys() if not el == 'dict_filename')
                dict2 = OrderedDict()

                for el in rs.keys():
                    if not el == 'dict_filename':
                        dict2[el] = " "

                for h in headers_list:
                    try:
                        h1 = None
                        if "_" in h:
                            h1 = str(h).split("_")[1]  # as level name is split from dim_level format and stored
                        else:
                            h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                    except:
                        print "Exception while adding tagged data to database"
                        print traceback.print_exc()
                #print(dict2)
                # aid = str(request) + str(row['rid'])

                rev_obj = Review.objects.get(rid=row['rid'])
                dict_name_obj = DimenMap.objects.get(dict_filename=dict_name)
                obj1 = TaggedDataRev.objects.create(rid=rev_obj, pCategory=request, ngram=str(row['ngram']), dict_filename=dict_name_obj, **dict2)
                obj1.save()
            print("Tagged output inserted into db")
        except:
            print("Couldn't insert into TaggedDataRev")
            print(traceback.print_exc())

        # Compute aggregated data and save into database ########################################
        agg_df = aggregate(tagged_df, request)
        print(agg_df)
        agg_df_cols = ['rid']
        agg_df_cols.extend(agg_df.columns)

        headers_list = [t for t in agg_df_cols if t not in ['rid', 'ngram']]
        # print(headers_list)
        try:
            for idx, row in agg_df.iterrows():
                dims_list = [k for k in rs.keys() if not k == 'dict_filename' and "_" not in k]
                # dict2 = OrderedDict((el, " ") for el in dims_list)
                dict2 = OrderedDict()
                # print dict2

                for el in rs.keys():
                    if not el == 'dict_filename' and not "_" in el:
                        dict2[el] = " "
                for h in headers_list:
                    try:
                        h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                    except:
                        print "Exception while adding agg tagged data to database"
                        print traceback.print_exc()
                # print(dict2)
                # aid = str(request) + str(row['rid'])

                rev_obj = Review.objects.get(rid=row['rid'])
                obj1 = AggTaggedDataRev.objects.create(rid=rev_obj, pCategory=request, **dict2)
                obj1.save()
            print("Agg tagged output inserted into db")
        except:
            print("Couldn't insert into AggTaggedDataRev")
            print(traceback.print_exc())

        statuscode = 200
    except:
        statuscode = 500

    return [agg_df, statuscode]


def main2(request, dictfile):
    statuscode = 500
    if ".csv" in request:
        request = str(request).split(".")[0]

    # source_df= pd.read_csv(sourcefile, dtype={'ARTICLE_ID': str})

    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    source_qs = Uploads.objects.filter(pCategory=request).values()

    print("source qs akshat", source_qs)
    source_df = pd.DataFrame.from_records(source_qs)

    print("source df akshat", source_df)
    ##########
    source_df = pd.DataFrame.from_records(source_qs)

    # source_df['rid'] = source_df['rid'].apply(lambda x: '%.0f' % x)  # formats the column to float
    source_df['rid'] = source_df['rid'].astype('str')  # formats the column to str

    # dict_df = dictfile
    dict_df = pd.read_csv(dictfile, encoding='utf-8')

    tagged_df_cols = ['rid']
    tagged_df_cols.extend(dict_df.columns)
    # print(tagged_df_cols)
    tagged_df = pd.DataFrame(columns=tagged_df_cols)

    # tagged_df['ARTICLE_ID'] = pd.to_numeric(tagged_df['ARTICLE_ID'], errors='coerce')
    # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype('float64)
    agg_df = None
    try:
        for s in source_qs:
            curr_conv = s['rText']
            curr_conv = clean_text(curr_conv)
            for i2, r2 in dict_df.iterrows():
                curr_entry = []
                # str_to_match = str(r2['ngram']).center(len(r2['ngram']) + 2, ' ')
                ng_to_match = str(r2['ngram'])
                ng_to_match = clean_ngram(ng_to_match)
                try:
                    # if str_to_match[:len(str_to_match)-2].lower() in curr_conv.lower():   # adds leading and trailing whitespaces to match as one phrase
                    mat = re.findall(ng_to_match.lower(), curr_conv.lower(), re.I)
                    if len(mat) > 0:
                        # print(ng_to_match, curr_conv)
                        # print(r1['ARTICLE_ID'])
                        curr_entry.append(str(s['rid']))
                        curr_entry.extend(r2.tolist())  # condition, slicing
                        # print(curr_entry)
                        tagged_df.loc[len(tagged_df)] = curr_entry
                except TypeError:
                    pass

        # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype(float)
        # df1 = df.apply(pd.to_numeric, args=('coerce',))

        # tagged_df = tagged_df.drop([t for t in tagged_df_cols if '_' in t and not t == 'rid'], axis=1)
        print(tagged_df)

        # Insert tagged data into database #############################################

        try:
            rs = DimenMap.objects.values().get(dict_filename=request)
        except:
            rs = DimenMap.objects.filter(dict_filename=request).values()[0:1]
            rs = rs[0]

        headers_list = [t for t in tagged_df_cols if t not in ['rid', 'ngram']]
        #print(headers_list)
        try:
            for idx, row in tagged_df.iterrows():
                # dict2 = OrderedDict((el, " ") for el in rs.keys() if not el == 'dict_filename')
                dict2 = OrderedDict()

                for el in rs.keys():
                    if not el == 'dict_filename':
                        dict2[el] = " "

                # print(dict2)

                for h in headers_list:
                    try:
                        h1 = None
                        if "_" in h:
                            h1 = str(h).split("_")[1]  # as level name is split from dim_level format and stored
                        else:
                            h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                    except:
                        print "Exception while adding tagged data to database"
                        print traceback.print_exc()
                #print(dict2)
                # aid = str(request) + str(row['rid'])

                upl_obj = Uploads.objects.get(rid=row['rid'])
                obj1 = TaggedDataUpl.objects.create(rid=upl_obj, dataset_filename=request, ngram=str(row['ngram']), **dict2)
                obj1.save()
            print("Tagged output inserted into db")
        except:
            print("Couldn't insert into TaggedData")
            print(traceback.print_exc())

        # Compute aggregated data and save into database ########################################
        agg_df = aggregate(tagged_df, request)
        print(agg_df)
        agg_df_cols = ['rid']
        agg_df_cols.extend(agg_df.columns)

        headers_list = [t for t in agg_df_cols if t not in ['rid', 'ngram']]
        # print(headers_list)
        try:
            for idx, row in agg_df.iterrows():
                dims_list = [k for k in rs.keys() if not k == 'dict_filename' and "_" not in k]

                # dict2 = OrderedDict((el, " ") for el in dims_list)
                # print(dict2)
                dict2 = OrderedDict()
                # print dict2

                for el in rs.keys():
                    if not el == 'dict_filename' and not "_" in el:
                        dict2[el] = " "
                for h in headers_list:
                    try:
                        h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                    except:
                        print "Exception while adding agg_tagged data to database"
                        # print traceback.print_exc()
                # print(dict2)
                # aid = str(request) + str(row['rid'])

                upl_obj = Uploads.objects.get(rid=row['rid'])
                obj1 = AggTaggedDataUpl.objects.create(rid=upl_obj, dataset_filename=request, **dict2)
                obj1.save()
            print("Agg tagged output inserted into db")
        except:
            print("Couldn't insert into AggTaggedDataUpl")
            print(traceback.print_exc())

        statuscode = 200
    except:
        statuscode = 500

    return [agg_df, statuscode]


def main3(request, sourcefile, dictfile):
    print("ngm main3")
    statuscode = 500
    if ".csv" in request:
        request = str(request).split(".")[0]
    print(request)
    # source_df= pd.read_csv(sourcefile, dtype={'ARTICLE_ID': str})

    # print(dictfile)
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    # source_df = pd.read_csv(sourcefile)

    # source_df = sourcefile
    source_df = pd.read_csv(StringIO(sourcefile), encoding='utf-8')
    # print(source_df)
    # source_df['rid'] = source_df['rid'].apply(lambda x: '%.0f' % x)  # formats the column to float
    source_df['rid'] = source_df['rid'].astype('str')  # formats the column to str
    # print(source_df['rid'])
    # dict_df = dictfile
    dict_df = pd.read_csv(dictfile, encoding='utf-8', engine='python')
    # print(dict_df)
    tagged_df_cols = ['rid']
    tagged_df_cols.extend(dict_df.columns)
    # print(tagged_df_cols)
    tagged_df = pd.DataFrame(columns=tagged_df_cols)

    # tagged_df['ARTICLE_ID'] = pd.to_numeric(tagged_df['ARTICLE_ID'], errors='coerce')
    # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype('float64)
    agg_df = None
    try:
        for i1, r1 in source_df.iterrows():
            curr_conv = r1['rText']
            curr_conv = clean_text(curr_conv)
            for i2, r2 in dict_df.iterrows():
                curr_entry = []
                # str_to_match = str(r2['ngram']).center(len(r2['ngram']) + 2, ' ')
                ng_to_match = str(r2['ngram'])
                ng_to_match = clean_ngram(ng_to_match)
                try:
                    # if str_to_match[:len(str_to_match)-2].lower() in curr_conv.lower():   # adds leading and trailing whitespaces to match as one phrase
                    mat = re.findall(ng_to_match.lower(), curr_conv.lower(), re.I)
                    if len(mat) > 0:
                        # print(ng_to_match, curr_conv)
                        # print(str(r2['ngram']), curr_conv)
                        curr_entry.append(str(r1['rid']))
                        curr_entry.extend(r2.tolist())  # condition, slicing
                        tagged_df.loc[len(tagged_df)] = curr_entry
                        # print(tagged_df[len(tagged_df)])
                except TypeError:
                    print("type error")
                    # print(traceback.print_exc())
                except:
                    print("other error")
                    # print(traceback.print_exc())
            # print("looped thru dict2 rows")
        # tagged_df['ARTICLE_ID'] = tagged_df['ARTICLE_ID'].astype(float)
        # df1 = df.apply(pd.to_numeric, args=('coerce',))
        # print("looped thru sourcedf")

        print(tagged_df)

        # Insert tagged data into database #############################################

        try:
            rs = DimenMap.objects.values().get(dict_filename=request)
        except:
            rs = DimenMap.objects.filter(dict_filename=request).values()[0:1]
            rs = rs[0]

        # print(rs)
        headers_list = [t for t in tagged_df_cols if t not in ['rid', 'ngram']]
        # print(headers_list)
        try:
            for idx, row in tagged_df.iterrows():
                # dict2 = OrderedDict((el, " ") for el in rs.keys() if not el == 'dict_filename' and not el == 'id')
                dict2 = OrderedDict()

                for el in rs.keys():
                    if not el == 'dict_filename':
                        dict2[el] = " "

                # print(dict2)
                for h in headers_list:
                    try:
                        h1 = None
                        if "_" in h:
                            h1 = str(h).split("_")[1]  # as level name is split from dim_level format and stored
                        else:
                            h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                    except:
                        print "Exception while adding tagged data to database"
                        print traceback.print_exc()
                # print(dict2)
                aid = str(request) + str(row['rid'])

                soc_obj = Social.objects.get(aid=aid)
                # print(soc_obj)
                obj1 = TaggedData.objects.create(aid=soc_obj, dataset_filename=request, rid=str(row['rid']), ngram=str(row['ngram']), **dict2)
                obj1.save()
            print("Tagged output inserted into db")
        except:
            print("Couldn't insert into TaggedData")
            # print(traceback.print_exc())

        print(" Now aggregating the mapping")

        # Compute aggregated data and save into database ########################################
        agg_df = aggregate(tagged_df, request)
        print(agg_df)
        agg_df_cols = ['rid']
        agg_df_cols.extend(agg_df.columns)
        headers_list = [t for t in agg_df_cols if t not in ['rid', 'ngram'] and "_" not in t]
        # print(headers_list)
        try:
            # print(" inside try")
            for idx, row in agg_df.iterrows():

                # dict2 = dict((el, " ") for el in rs.keys() if el not in ['dict_filename', 'id'] and not "_" in el)
                dict2 = OrderedDict()
                # print dict2

                for el in rs.keys():
                    if not el == 'dict_filename' and not "_" in el:
                        dict2[el] = " "

                # print(dict2)
                for h in headers_list:
                    try:
                        # print(h)
                        h1 = h

                        # assigns the value of curr header of tag_dict_df row, >>> row[h]  >>> rhs
                        # to the key of dict2, such that  >>>  dict2[<...>] = ...  >>> lhs
                        # it is the same key as that in dict1,   >>> dict1.keys()[...]  >>> outermost box bracket of lhs
                        # which has the same value as the value of curr header of tag_dict_df row   >>> dict1.values().index(row[h])   >>> inner box bracket of lhs
                        # print(str(row[h]))
                        # print(rs.values().index(h1))
                        # print(rs.keys()[rs.values().index(h1)])

                        dict2[rs.keys()[rs.values().index(h1)]] = row[h]

                        # print("dict2 updated")
                    except:
                        # pass
                        print "Exception while adding agg_tagged data to database"
                        print traceback.print_exc()
                # print(dict2)
                aid = str(request) + str(row['rid'])

                soc_obj = Social.objects.get(aid=aid)
                # print(soc_obj)
                obj1 = AggTaggedData.objects.create(aid=soc_obj, dataset_filename=request, rid=str(row['rid']), **dict2)
                obj1.save()

                # print(" obj saved")
            print("Agg tagged output inserted into db")

        except:
            print("Couldn't insert into AggTaggedData")
            print(traceback.print_exc())

        print ("Exiting Ngram mapping")
        statuscode = 200
    except:
        print("except")
        print(traceback.print_exc())
        statuscode = 500

    return [agg_df, statuscode]

