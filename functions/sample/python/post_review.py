#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_cloud_sdk_core import ApiException
# import requests
# from requests.exceptions import ConnectionError, ReadTimeout, RequestException

def main(dict):
    DB_NAME='reviews'
    try:
        authenticator = IAMAuthenticator("VHPowScjpMEuMvqdJHGV7t2vyhoQP_sWukDkhlJ-OOga")
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url('https://32b60b7a-3008-49d8-9c8a-e9c4703fd00f-bluemix.cloudantnosqldb.appdomain.cloud')
        
        response = service.post_document(
            db=DB_NAME,
            document=dict['review']).get_result()

        print('Post Review: ',response)
        
    except Exception as e:  
        message = "Something went wrong"+e.message 
        return {
            'statusCode':500,
            'error':message,
            'queryparams':json.dumps(query_params)
        }

    return {
        'statusCode':200,
        'headers': { 'Content-Type': 'application/json' },
        "result": response
    }

