import django
django.setup()
import requests
import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from atlas.config import dbConfig
import traceback
import sys


reload(sys)
sys.setdefaultencoding('utf8')


def callZeppelin(kw):
    url = 'http://172.16.15.4:8080/#/notebook/2DTP82UXX'

    r = requests.get(url)  # , params=params, headers=headers)
    try:
        file1 = open(dbConfig.dict['zepPath'], "w+")
        file1.write(r.text)
        file1.close()
        print("HTML file saved")
        print(str(r.text))
    except:
        print("Error while saving html")
        print(traceback.print_exc())

    list_resp = [r.text]
    data_json = json.dumps(list_resp)

    return HttpResponse(data_json)


