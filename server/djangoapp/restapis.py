import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    try:
        # Call get method of requests library with URL and parameters
       
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                        params=kwargs)
        print('Response json: ',json.dumps(response.json()))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f'With status {status_code}')

    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url,json_payload, **kwargs):
    print(f'post_request kwargs: {kwargs}')
    print(f'Post Review JSON payload: {json.dumps(json_payload)}')
    print(f"POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        print('Response json: ',json.dumps(response.json()))
    except:
        print("network exception occurred")
    status_code = response.status_code
    print(f'With status {status_code}')
    json_data = json.loads(response.text)
    return json.dumps(response.json())

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter

    json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            if 'language' in dealer_doc and dealer_doc['language']== 'query':
                continue
            print(f'dealer_doc: {json.dumps(dealer_doc)}')
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state= dealer_doc['state'], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_id(url, dealerId):
    
    json_result = get_request(url,id=dealerId)

    if json_result:
        # Get the row list in JSON as dealers
        if len(json_result['result']) > 0 :
            dealer = json_result["result"][0]
        # For each dealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                        id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                        short_name=dealer["short_name"],st=dealer["st"], state= dealer['state'], zip=dealer["zip"])
        
            return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
    results = []
    json_result = get_request(url,dealerId = dealerId)
    if json_result:
        review_list = json_result["result"]["docs"]
        # - Parse JSON results into a DealerView object list
        for review in review_list:
            sentiment=analyze_review_sentiments(review['review'])
            review_obj = DealerReview(review['id'],review['dealership'],review['name'],review['purchase'],review['review'],
            sentiment)
            if review['purchase']== True:
                review_obj.car_make = review['car_make']
                review_obj.purchase_date = review['purchase_date']
                review_obj.car_model = review['car_model']
                review_obj.car_year = review['car_year']

            results.append(review_obj)
    return results

# Get all reviews from cloud function
def get_all_reviews_from_cf(url):
# - Call get_request() with specified arguments
    results = []
    json_result = get_request(url)
    if json_result:
        review_list = json_result["result"]["rows"]
        # - Parse JSON results into a DealerView object list
        count = 0
        for review in review_list:
            if 'dealership' in review['doc'] :
                count += 1
            
        print(f'Total Number of reviews : {count}')
    return count

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
    API_KEY='oNrpe3RdkwQGhKsyTo4AlhjT3EjQCrTQ6nR8o1nxW-kK'
    URL='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/daa4f8dc-59eb-43aa-8dd1-e2ebee73e3df'
    
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(URL)

    print(f'Analyzing sentiment for : {text}')
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(targets=[text])),
        language='en'
        ).get_result()

    print(f'Sentiment response: {json.dumps(response)}')
    return response['sentiment']['document']['label']
# - Get the returned sentiment label such as Positive or Negative



