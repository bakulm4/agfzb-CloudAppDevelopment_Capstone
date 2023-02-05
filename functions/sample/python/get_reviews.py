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
import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(param_dict):
    IAM_API_KEY = 'VHPowScjpMEuMvqdJHGV7t2vyhoQP_sWukDkhlJ-OOga';
    COUCH_URL = 'https://32b60b7a-3008-49d8-9c8a-e9c4703fd00f-bluemix.cloudantnosqldb.appdomain.cloud';
    DB_NAME = 'reviews'

    authenticator = IAMAuthenticator(IAM_API_KEY)
    service = CloudantV1(authenticator=authenticator)

    service.set_service_url(COUCH_URL)
    
    if "dealerId" in param_dict :
        return get_matching_records(service,DB_NAME,{"dealership":{"$eq":param_dict["dealerId"]}},param_dict);

    return get_all_records(service,DB_NAME)

def get_matching_records(cloudant,dbname,selector,query_params):
    try:
        response = cloudant.post_find(db=dbname,selector=selector,execution_stats=True).get_result()
        if len(response['docs']) > 0 :
            code = 200
        else:
            code = 404
        return {
            'statusCode':code,
            'headers': { 'Content-Type': 'application/json' },
            'result':{'params':json.dumps(query_params),'data':response}
        }
    except Exception as e:  
        message = "Something went wrong"+e.message 
        return {
            'statusCode':500,
            'error':message,
            'queryparams':json.dumps(query_params)
        }

def get_all_records(cloudant, dbname):
    try:
        response = cloudant.post_all_docs(db=dbname,include_docs=True,limit=10).get_result()
        if len(response) > 0 :
            code = 200
        else:
            code = 404
        return {
            'statusCode':code,
            'headers': { 'Content-Type': 'application/json' },
            'result':response
        }
    except Exception as e:  
        message = "Something went wrong"+e.message 
        return {
            'statusCode':500,
            'error':message
        }

