# import json
# from django.core.serializers.json import DjangoJSONEncoder
import django
django.setup()
import requests


def getRevClusteringData(kw, engine):
    # url = 'http://35.227.67.93/solr/MY_PRODUCT/clustering'
    url = 'http://35.231.181.187/solr/CORE_ATLAS_REV/clustering'
    params = {'q': 'pCategory:' + kw, 'clustering.engine': engine, 'wt': 'json', 'indent': 'on'}

    username = "user"
    password = "IBpc7CXPlxKp"
    combined_cred = username + ":" + password
    hashed_code = combined_cred.encode('base64')[:-2]
    # hashed_code = base64.encodestring(combined_cred)
    print(hashed_code)

    # Create your header as required
    headers = {"Content-Type": "application/json", "Authorization": "Basic " + hashed_code,
               "Access-Control-Allow-Origin": "*"}

    r = requests.get(url, params=params, headers=headers)
    print(r)
    return r


def getSocClusteringData(kw, engine):
    # url = 'http://35.227.67.93/solr/MY_PRODUCT3_1/clustering'
    url = 'http://35.231.181.187/solr/CORE_ATLAS_SOC/clustering'
    params = {'q': 'dataset_filename:' + kw, 'clustering.engine': engine, 'wt': 'json', 'indent': 'on'}

    username = "user"
    password = "IBpc7CXPlxKp"
    combined_cred = username + ":" + password
    hashed_code = combined_cred.encode('base64')[:-2]
    # hashed_code = base64.encodestring(combined_cred)
    print(hashed_code)

    # Create your header as required
    headers = {"Content-Type": "application/json", "Authorization": "Basic " + hashed_code,
               "Access-Control-Allow-Origin": "*"}

    r = requests.get(url, params=params, headers=headers)
    print(r)
    return r


def getUplClusteringData(kw, engine):
    # url = 'http://35.227.67.93/solr/MY_PRODUCT3/clustering'
    url = 'http://35.231.181.187/solr/CORE_ATLAS_UPL/clustering'
    params = {'q': 'pCategory:' + kw, 'clustering.engine': engine, 'wt': 'json', 'indent': 'on'}

    username = "user"
    # password = "DwC13babY5yj"
    password = "IBpc7CXPlxKp"
    combined_cred = username + ":" + password
    hashed_code = combined_cred.encode('base64')[:-2]
    # hashed_code = base64.encodestring(combined_cred)
    print(hashed_code)

    # Create your header as required
    headers = {"Content-Type": "application/json", "Authorization": "Basic " + hashed_code,
               "Access-Control-Allow-Origin": "*"}

    r = requests.get(url, params=params, headers=headers)
    print(r)
    return r


def getFullImport():
    core_names = ['CORE_ATLAS_REV', 'CORE_ATLAS_UPL', 'CORE_ATLAS_SOC']
    status_codes = []
    # url = 'http://35.227.67.93/solr/MY_PRODUCT3_1/clustering'
    for cn in core_names:
        try:
            url = 'http://35.231.181.187/solr/'+ cn +'/dataimport'
            params = {'command': 'full-import', 'wt': 'json', 'indent': 'on'}

            username = "user"
            password = "IBpc7CXPlxKp"
            combined_cred = username + ":" + password
            hashed_code = combined_cred.encode('base64')[:-2]
            # hashed_code = base64.encodestring(combined_cred)
            print(hashed_code)

            # Create your header as required
            headers = {"Content-Type": "application/json", "Authorization": "Basic " + hashed_code,
                       "Access-Control-Allow-Origin": "*"}

            r = requests.get(url, params=params, headers=headers)
            print(r)
            status_codes.append(200)
        except:
            status_codes.append(500)
    return status_codes