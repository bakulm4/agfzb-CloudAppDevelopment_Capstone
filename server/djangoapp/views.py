from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealers_by_id, get_dealer_reviews_from_cf, post_request, get_all_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/get-dealership.json'
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context['dealership_list']=dealerships
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request,'djangoapp/index.html',context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
# ...
 if request.method == "GET":
        context = {}

        get_reviews_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/get-review.json'
        get_dealer_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/get-dealership.json'

        dealer = get_dealers_by_id(get_dealer_url,dealer_id)
        reviews = get_dealer_reviews_from_cf(get_reviews_url,dealer_id)
        if dealer :
            context['review_list'] = reviews
            context['dealer'] = dealer
        #review_list = ' \n'.join([review.__str__() for review in reviews])

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
# ...
    user = request.user
    context = {}
    post_review_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/post-review.json'
    
    get_dealer_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/get-dealership.json'
    get_reviews_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/6993893f-7c4d-4925-9ff9-fd838b5abddf/dealership-package/get-review.json'
  
    review_count = get_all_reviews_from_cf(get_reviews_url)
    car_model_list = CarModel.objects.filter(dealer_id=dealer_id)
    print(f'Car model list: {car_model_list}')
    if user.is_authenticated:
        if request.method == "GET":
            dealer = get_dealers_by_id(get_dealer_url,dealer_id)
            if dealer :
                context['dealer'] = dealer

            context['cars'] = car_model_list

            return render(request, 'djangoapp/add_review.html',context) 

        else:
            print(f'Form data: {list(request.POST.items())}')
            selected_car = CarModel.objects.get(pk=int(request.POST.get('car')))
            print(f'Selected Car: {selected_car}')
            review = {
                'id' : review_count+1,
                'name' : f'{request.user.first_name} {request.user.last_name}',
                'dealership' : dealer_id,
                'review' : request.POST['content'],
                'purchase': True if 'purchasecheck' in request.POST else False,
                'purchase_date' : request.POST['purchasedate'],
                'car_make' : selected_car.make.name,
                'car_model' : selected_car.name,
                'car_year' : selected_car.year.year,
                'time' : datetime.utcnow().isoformat()
            }

            json_payload={
                'review':review
            }

            post_response = post_request(post_review_url, json_payload, dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)