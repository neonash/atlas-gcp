from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import ATLAS1
import ATLAS_v2
from atlas.config import dbConfig
import pandas as pd
import ContentCategories
import NgramMapping
import SentimentAnalysis_2
import TrigDriv_2
import TopicModeling
import logging
import traceback
from StringIO import StringIO
from atlas.models import Requests


def caller_file(full_data_dict):
    #print(full_data_dict)
    request = full_data_dict['filename_obj']
    print("Entering File analysis", request)
    filecontents = full_data_dict['file_data']
    # print("filecontents:", filecontents)
    # tag_dict = full_data_dict['tag_dict']

    #db = pymongo.MongoClient().atlas
    #s = request.encode('utf-8')

    df = pd.read_csv(dbConfig.dict["requestUrl"], encoding='utf-8')
    status_dict = {'status': None, "senti_list": None, 'td_list': None}
    print("going to read file contents into df.")
    file_contents_df = pd.read_csv(StringIO(filecontents), encoding='utf-8')
    print("file contents read into df.")

    if "pCategory" in file_contents_df.columns.values.tolist():
        print("Calling Atlas1.main2()")
        status = ATLAS1.main2(request, filecontents, full_data_dict['tag_dict'])
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '15% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
        df.ix[(df.reqKw == request), 'reqStatus'] = "15% complete"

        # file_dict = {
        #     '_id': binascii.hexlify(s),
        #     'Product': request,
        #
        #     'metadata': {
        #         '_id': binascii.hexlify(s),
        #         'lastUpdated': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p"),
        #         'name': request
        #     },
        #     'analyticData': {
        #         'sentimentData': [
        #
        #         ],
        #         'trigdrivData': {
        #
        #         }
        #     }
        # }
        # result = db.data.insert_one(file_dict)
        # sent_list = SentimentAPI_generic.senti_main(dbConfig.dict['uploadsUrl'] + request, ',')
        # print sent_list
        #
        # target_string = "analyticData.sentimentData"
        #
        # db.data.update({"_id": binascii.hexlify(s)}, {"$set": {target_string: sent_list[0]}})
        # print result.inserted_id

        # Calling analyses files - sentiment, trigger/driver and topic modelling
        try:
            print("Now classifying content categories")
            cc_list = ContentCategories.main(request)
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '35% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "35% complete"
        except:
            print("Error while classifying content categories")
            print(traceback.print_exc())

        # Calling analyses files - sentiment, trigger/driver and topic modelling
        try:
            print("Now tagging the dataset")
            tagop_list = NgramMapping.main2(request, full_data_dict['tag_dict'])
            #tagop_list = NgramMapping.main2("headphones", full_data_dict['tag_dict'])
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '50% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "50% complete"
        except:
            print("Error while tagging dataset with dictionary")
            print(traceback.print_exc())

        try:
            print("Calling sentiment analyses to run on uploaded file...")
            sent_list = SentimentAnalysis_2.senti_main2(request, filecontents, full_data_dict['senti_dict'])
            #print sent_list
            print("Sentiment data inserted into DB")
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '65% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "65% complete"

        except:
            print("Error while analysing sentiment")
            #print(traceback.print_exc())

        try:
            td_list = TrigDriv_2.td_main2(request, full_data_dict['td_dict'])
            #print td_list
            print("TriggerDriver data inserted into DB")
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '80% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "80% complete"
        except:
            print("Error while analysing triggers/drivers")
            #print(traceback.print_exc())

    else:
        print("Calling Atlas1.main3()")
        # if 'supplements_10k_1' not in request:
        status = ATLAS1.main3(request, filecontents, full_data_dict['tag_dict'])
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '15% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
        df.ix[(df.reqKw == request), 'reqStatus'] = "15% complete"

        # Calling analyses files - sentiment, trigger/driver and topic modelling
        try:
            print("Now classifying content categories")
            cc_list = ContentCategories.main(request)
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '35% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "35% complete"
        except:
            print("Error while classifying content categories")
            print(traceback.print_exc())

        # Calling analyses files - sentiment, trigger/driver and topic modelling
        try:
            print("Now tagging the dataset with the dictionary provided")
            tagop_list = NgramMapping.main3(request, full_data_dict['file_data'], full_data_dict['tag_dict'])
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '50% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "50% complete"
        except:
            print("Error while tagging dataset with dictionary")
            print(traceback.print_exc())

        try:
            print("Calling sentiment analyses to run on uploaded file...")
            sent_list = SentimentAnalysis_2.senti_main3(request, filecontents, full_data_dict['senti_dict'])
            # print sent_list
            print("Sentiment data inserted into DB")
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '65% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "65% complete"

        except:
            print("Error while analysing sentiment")
            # print(traceback.print_exc())

        try:
            td_list = TrigDriv_2.td_main3(request, full_data_dict['td_dict'])
            # print td_list
            print("TriggerDriver data inserted into DB")
            try:
                req_obj = Requests.objects.get(reqKw=request)
                req_obj.reqStatus = '80% complete'
                req_obj.save()
            except:
                print("Couldn't save status update in DB!")
                print(traceback.print_exc())
            df.ix[(df.reqKw == request), 'reqStatus'] = "80% complete"
        except:
            print("Error while analysing triggers/drivers")
            # print(traceback.print_exc())
        # else:
        #     try:
        #         print("Now tagging the supplements dataset with the dictionary provided")
        #         tagop_list = NgramMapping.main3(request, full_data_dict['file_data'], full_data_dict['tag_dict'])
        #     except:
        #         print("Error while tagging supplement dataset with dictionary")
        #         print(traceback.print_exc())

    print "Going to topic model"
    # Performing Topic Modeling Analysis
    num_topics = 8
    topic_status = TopicModeling.main(request, num_topics)
    try:
        req_obj = Requests.objects.get(reqKw=request)
        req_obj.reqStatus = 'Complete'
        req_obj.save()
    except:
        print("Couldn't save status update in DB!")
        print(traceback.print_exc())
    df.ix[(df.reqKw == request), 'reqStatus'] = "Complete"

    # if status == 200 and sent_list == 200 and td_list == 200 and topic_status == 200:
    #     # Update request csv status to completed
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Completed"
    # elif status == 200 and sent_list == 200 and td_list == 200:
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Topic Modelling Failed"
    # elif status == 200 and sent_list == 200:
    #         df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Trigger/Driver Failed"
    # elif status == 200:
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Sentiment Failed"
    # else:
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Scraping incomplete"

    with open(dbConfig.dict["requestUrl"], 'w') as f:
        df.to_csv(f, index=False)

    print("Exiting return")
    return request


def caller(request, site, full_data_dict):
    print(full_data_dict['tag_dict'])  # dict with default dict urls for automatic scraped data tagging
    print("Entering", request, site)
    # df = pd.read_csv(dbConfig.dict["requestUrl"], encoding='utf-8')
    # db = pymongo.MongoClient().atlas
    # s = request.encode('utf-8')

    status = ATLAS_v2.main(request, site)
    print("Atlas main finish")
    try:
        req_obj = Requests.objects.get(reqKw=request)
        req_obj.reqStatus = '15% complete'
        req_obj.save()
    except:
        print("Couldn't save status update in DB!")
        print(traceback.print_exc())
    # df.ix[(df.reqKw == request), 'reqStatus'] = "20% complete"

    # Calling analyses files - sentiment, trigger/driver and topic modelling
    try:
        print("Now classifying content categories")
        cc_list = ContentCategories.main(request)
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '35% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
            # df.ix[(df.reqKw == request), 'reqStatus'] = "40% complete"
    except:
        print("Error while classifying content categories!")
        print(traceback.print_exc())

    # Calling analyses files - sentiment, trigger/driver and topic modelling
    try:
        print("Now tagging the dataset...")
        tagop_list = NgramMapping.main(request, full_data_dict['tag_dict'])
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '50% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
        # df.ix[(df.reqKw == request), 'reqStatus'] = "40% complete"
    except:
        print("Error while tagging dataset with dictionary")
        print(traceback.print_exc())

    try:
        sent_list = SentimentAnalysis_2.senti_main(request)
        #print sent_list
        print("Sentiment data inserted into DB")
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '65% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
        # df.ix[(df.reqKw == request), 'reqStatus'] = "60% complete"
    except:
        print("Error while analysing sentiment")
        print(traceback.print_exc())


    try:
        td_list = TrigDriv_2.td_main(request)
        #print td_list
        print("TriggerDriver data inserted into DB")
        try:
            req_obj = Requests.objects.get(reqKw=request)
            req_obj.reqStatus = '80% complete'
            req_obj.save()
        except:
            print("Couldn't save status update in DB!")
            print(traceback.print_exc())
        # df.ix[(df.reqKw == request), 'reqStatus'] = "80% complete"
    except:
        print("Error while analysing triggers/drivers")
        print(traceback.print_exc())

    print "Going to topic model"
    #logging.info("going to topicmodeling.main")
    #
    #Performing Topic Modeling Analysis
    num_topics = 8
    topic_status = TopicModeling.main(request, num_topics)

    # df = pd.read_csv(dbConfig.dict["requestUrl"], encoding='utf-8')
    # if status == 200 & sent_list[1] == 200 & topic_status == 200:
    #     # Update request csv status to completed
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Completed"
    # else:
    #     df.ix[(df.reqKw == request) & (df.reqStatus == 'Pending'), 'reqStatus'] = "Failed"
    try:
        req_obj = Requests.objects.get(reqKw=request)
        req_obj.reqStatus = 'Complete'
        req_obj.save()
    except:
        print("Couldn't save status update in DB!")
        print(traceback.print_exc())
    # df.ix[(df.reqKw == request), 'reqStatus'] = "Complete"
    # with open(dbConfig.dict["requestUrl"], 'w') as f:
    #     df.to_csv(f, index=False)

    print("Exiting Return")
    return request


pool = ProcessPoolExecutor()


def pool_exe(request, site, full_data_dict):  # to Rev
    future = pool.submit(caller, request, site, full_data_dict)
    print ("Exit pool exe\n")


#def pool_exe_file(request,filecontents):
#    future = pool.submit(caller_file, request, filecontents)
#    print("Exit file pool exe\n")


def pool_exe_file(full_data_dict):  # to Upl, Soc
    future = pool.submit(caller_file, full_data_dict)
    print("Exit file pool exe\n")
