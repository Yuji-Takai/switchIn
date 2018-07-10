from django.db import models

# Coverage:             represents the coverage of user's policy
# liability_property:   property damage liability limit
# liability_person:     bodily injury liability limit per person
# liability_accident:   bodily injury liability limit per accident
# personal_injury:      personal injury protectino deductible
# comprehensive:        comprehensive deductible
# collision:            collision deductible
# uninsured_property:   uninsured motorist property damage limit
# uninsured_person:     uninsured motorist injury limit per person
# uninsured_accident:   uninsured motorist injury limit per accident
# under_property:       uninsured/underinsured motorist property damage limit
# under_person:         uninsured/underinsured motorists per person limit
# under_accident:       uninsured/underinsured motorists per accident limit
class Coverage(models.Model):
    liability_property = models.PositiveIntegerField(blank=True, default=0)
    liability_person   = models.PositiveIntegerField(blank=True, default=0)
    liability_accident = models.PositiveIntegerField(blank=True, default=0)
    personal_injury    = models.PositiveIntegerField(blank=True, default=0)
    comprehensive      = models.PositiveIntegerField(blank=True, default=0)
    collision          = models.PositiveIntegerField(blank=True, default=0)
    uninsured_property = models.PositiveIntegerField(blank=True, default=0)
    uninsured_person   = models.PositiveIntegerField(blank=True, default=0)
    uninsured_accident = models.PositiveIntegerField(blank=True, default=0)
    under_property     = models.PositiveIntegerField(blank=True, default=0)
    under_person       = models.PositiveIntegerField(blank=True, default=0)
    under_accident     = models.PositiveIntegerField(blank=True, default=0)

# Vehicle:              represents a vehice covered under user's policy
# name:                 vehicle's make model year
# make:                 vehicle's make
# model:                vehicle's model
# year:                 vehicle's year
# mass:                 vehicle's mass (in kg)
# iso_coll:             vehicle's collision ISO (1 - 10)
# iso_comp:             vehicle's comprehensive ISO (1 - 10)
class Vehicle(models.Model):
    name     = models.CharField(max_length=46, primary_key=True)
    make     = models.CharField(max_length=20, null=True)
    model    = models.CharField(max_length=20, null=True)
    year     = models.PositiveIntegerField(blank=True, default=1990)
    mass     = models.PositiveIntegerField(blank=True, default=0)
    iso_coll = models.PositiveIntegerField(blank=True, default=5)
    iso_comp = models.PositiveIntegerField(blank=True, default=5)
    def __str__(self):
        return self.name

# State:                represents a state
# name:                 name of the state (Rhode Island has the longest name)
# name_abbrev:          abbreviation of the name
# min_coverage:         minimum coverage requirement
# avg_property:         average property damage cost
# avg_fatal:            average fatal injury cost
# fatal_num:            number of fatal injury accidents per year
# avg_severe:           average severe injury cost
# severe_num:           number of severe injury accidents  per year
# avg_visible:          average visible injury cost
# visible_num:          number of visible injury accidents per year
# avg_pain:             average complain of pain cost
# pain_num:             number of compalin of pain accidents per year
# avg_mileage:          average mileage driven in the state
# pop_vehicle:          most registered vehicle in the year
# total_pop:            total population
# vehicle_pop:          total number of vehicles in the state
# uninsured_rate:       ratio of uninsured driver population to total driver population
class State(models.Model):
    name         = models.CharField(max_length=12, null=True)
    name_abbrev  = models.CharField(max_length=2, primary_key=True)
    # min_coverage = models.OneToOneField(Coverage, on_delete=models.CASCADE, null=True)
    avg_property = models.PositiveIntegerField(default=0)
    avg_fatal    = models.PositiveIntegerField(default=0)
    fatal_num    = models.PositiveIntegerField(default=0)
    avg_severe   = models.PositiveIntegerField(default=0)
    severe_num   = models.PositiveIntegerField(default=0)
    avg_visible  = models.PositiveIntegerField(default=0)
    visible_num  = models.PositiveIntegerField(default=0)
    avg_pain     = models.PositiveIntegerField(default=0)
    pain_num     = models.PositiveIntegerField(default=0)
    avg_mileage  = models.PositiveIntegerField(default=0)
    pop_vehicle  = models.CharField(max_length=46, default="general")
    total_pop    = models.PositiveIntegerField(default=0)
    vehicle_pop  = models.PositiveIntegerField(default=0)
    uninsured_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    def __str__(self):
        return self.name

# City:                 represents a city
# state:                state that the city belongs to
# name:                 name of the city
# crime_rate:           number of crime per driver
class City(models.Model):
    state       = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=40, primary_key=True)
    crime_rate  = models.DecimalField(max_digits=10, decimal_places=3)
    def __str__(self):
        return self.name

# Policy:               represents the user's policy
# company_name:         name of the insurance company
# policy_number:        policy number of the policy
# effective_date:       starting date of the policy
# expiration_date:      end date of the policy
# state:                state where the policy was issued
# coverage:             coverage of the policy
# vin:                  VIN of the vehicle
# mileage:              mileage driven per year by user
class Policy(models.Model):
    company_name    = models.CharField(max_length=40, null=True)
    policy_number   = models.CharField(max_length=30, null=True)
    effective_date  = models.DateField(auto_now=False, auto_now_add=False, null=True)
    expiration_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    coverage        = models.OneToOneField(Coverage, on_delete=models.CASCADE, null=True)
    vin             = models.CharField(max_length=17, null=True)
    mileage         = models.PositiveIntegerField(blank=True, default=0)
    vehicle         = models.CharField(max_length=46, default="general")
    city            = models.CharField(max_length=40, default="general")


class PolicyDoc(models.Model):
    city = models.CharField(max_length=40, default="general")
    mileage = models.PositiveIntegerField(blank=True, default=0)
    document = models.FileField(upload_to='uploads/')
