from django.db import models

# Coverage:             represents the coverage of user's policy
# liability_property:   property damage liability limit
# liability_injury:     bodily injury liability limit
# personal_injury:      personal injury protectino deductible
# comprehensive:        comprehensive deductible
# collision:            collision deductible
# uninsured_injury:     uninsured/underinsured motorist limit
class Coverage(models.Model):
    liability_property = models.CharField(max_length=200)
    liability_injury = models.CharField(max_length=200)
    personal_injury = models.CharField(max_length=200)
    comprehensive = models.CharField(max_length=200)
    collision = models.CharField(max_length=200)
    uninsured_injury = models.CharField(max_length=200)
    # uninsured/underinsured motorist property damage limit
    #uninsured_property = models.CharField(max_length=200)
    # full or deductible for emergency road service
    #road_service = models.CharField(max_length=200)
    # rental reimbursement
    #rental = models.CharField(max_length=200)

# Vehicle:              represents the vehice covered under user's policy
# year:                 year of the vehicle
# make:                 make of the vehicle
# model:                model of the vehicle
# vin:                  VIN of the vehicle
class Vehicle(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    vin = models.CharField(max_length=30)

# Policy:               represents the user's policy
# company_name:         name of the insurance company
# policy_number:        policy number of the policy
# effective_date:       starting date of the policy
# expiration_date:      end date of the policy
# state:                state where the policy was issued
# coverage:             coverage of the policy
# vehicle:              vehicle covered by the policy
class Policy(models.Model):
    company_name = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=30)
    effective_date = models.CharField(max_length=30)
    expiration_date = models.CharField(max_length=30)
    state = models.CharField(max_length=20, null=True)
    coverage = models.OneToOneField(Coverage, on_delete=models.CASCADE, null=True)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True)

class PolicyDoc(models.Model):
    document = models.FileField(upload_to='uploads/')
