import json, os
import requests
import datetime
import hmac
import hashlib
import base64

from django.conf import settings

def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data)


def get_json_file(json_file):

    if True or settings.LOCAL or settings.JSONFILES_STORAGE_CONTAINER == "":
        print("Loading local jsonfile")
        with open(os.path.join(settings.BASE_DIR, 'CMS/static/jsonfiles/' + json_file)) as json_file:
            data = json_file.read()

        response = requests.Response()

        response_state = response.__getstate__()
        response_state["status_code"] = 200
        response_state["_content"] = data.encode('utf-8')
        response_state["encoding"] = 'utf-8'
        
        response.__setstate__(response_state)

        return response
    
    # blob_name = json_file
    # container_name='jsonfiles'
    # api_version = '2019-12-12'
    # request_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    # storage_account_name = settings.STORAGE_ACCOUNT_NAME
    # storage_account_key = settings.STORAGEKEY
    
    # print('storage_account_name: {}'.format(storage_account_name))
    # print('storage_account_key: {}'.format(storage_account_key))
    # print('blob_name: {}'.format(blob_name))

    # string_params = {
    #     'verb': 'GET',
    #     'Content-Encoding': '',
    #     'Content-Language': '',
    #     'Content-Length': '',
    #     'Content-MD5': '',
    #     'Content-Type': '',
    #     'Date': '',
    #     'If-Modified-Since': '',
    #     'If-Match': '',
    #     'If-None-Match': '',
    #     'If-Unmodified-Since': '',
    #     'Range': '',
    #     'CanonicalizedHeaders': 'x-ms-date:' + request_time + '\nx-ms-version:' + api_version + '\n',
    #     'CanonicalizedResource': '/' + storage_account_name + '/'+ container_name + '/' + blob_name
    # }
    # print("'CanonicalizedResource': /{}/{}/{} ".format(storage_account_name,container_name,blob_name))
    # print('string_params: {}'.format(string_params))

    # string_to_sign = (string_params['verb'] + '\n' 
    #                 + string_params['Content-Encoding'] + '\n'
    #                 + string_params['Content-Language'] + '\n'
    #                 + string_params['Content-Length'] + '\n'
    #                 + string_params['Content-MD5'] + '\n' 
    #                 + string_params['Content-Type'] + '\n' 
    #                 + string_params['Date'] + '\n' 
    #                 + string_params['If-Modified-Since'] + '\n'
    #                 + string_params['If-Match'] + '\n'
    #                 + string_params['If-None-Match'] + '\n'
    #                 + string_params['If-Unmodified-Since'] + '\n'
    #                 + string_params['Range'] + '\n'
    #                 + string_params['CanonicalizedHeaders']
    #                 + string_params['CanonicalizedResource'])

    # signed_string = base64.b64encode(hmac.new(base64.b64decode(storage_account_key), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode()

    # headers = {
    #     'x-ms-date' : request_time,
    #     'x-ms-version' : api_version,
    #     'Authorization' : ('SharedKey ' + storage_account_name + ':' + signed_string)
    # }   
    
    # print('headers: {}'.format(headers))

    # url = 'https://' + storage_account_name + '.blob.core.windows.net/'+container_name+'/'+blob_name
    # r = requests.get(url, headers = headers)
    # print(r)
    # return r