from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(blank=False,max_length=15)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Make: {self.name}'


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'SD'
    SUV = 'SV'
    MINIVAN = 'MV'
    WAGON = 'WG'
    TRUCK = 'TR'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (MINIVAN, 'Minivan'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck'),
    ]
    type = models.CharField(
        max_length=2,
        choices=CAR_TYPE_CHOICES,
        default=SEDAN,
    )
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(blank=False,max_length=15)
    dealer_id = models.IntegerField(blank=True)
    year = models.DateField(null=True)

    def __str__(self):
        return f'Model: {self.name} Make: {self.make} Year: {self.year.year}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state abbrev
        self.st = st
        # Dealer state abbrev
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, dealership, name, purchase, review, sentiment, purchase_date = None, car_make=None, car_model=None, car_year=None):
        # Dealer address

        self.dealership = dealership
        # Dealer city
        self.name = name
        # Dealer Full Name
        self.purchase = purchase
        # Dealer id
        self.id = id
        # Location lat
        self.review = review
        # Location long
        self.car_year = car_year
        # Dealer short name
        self.purchase_date = purchase_date
        # Dealer state abbrev
        self.car_make = car_make
        # Dealer state abbrev
        self.car_model = car_model
        # Dealer zip
        self.sentiment = sentiment

    def __str__(self):
        return f"Review for {self.car_make} {self.car_model} ({self.car_year}) by {self.name}: {self.review}; sentiment: {self.sentiment} "