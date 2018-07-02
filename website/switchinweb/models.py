from django.db import models

class Coverage(models.Model):
    # property damage liability limit
    liability_property = models.CharField(max_length=200)
    # bodily injury liability limit
    liability_injury = models.CharField(max_length=200)
    # personal injury protection deductible
    personal_injury = models.CharField(max_length=200)
    # comprehensive deductible
    comprehensive = models.CharField(max_length=200)
    # collision deductible
    collision = models.CharField(max_length=200)
    # uninsured/underinsured motorist injury limit
    uninsured_injury = models.CharField(max_length=200)
    # uninsured/underinsured motorist property damage limit
    #uninsured_property = models.CharField(max_length=200)
    # full or deductible for emergency road service
    #road_service = models.CharField(max_length=200)
    # rental reimbursement
    #rental = models.CharField(max_length=200)

class Vehicle(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    vin = models.CharField(max_length=30)

class Policy(models.Model):
    company_name = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=30)
    effective_date = models.CharField(max_length=30)
    expiration_date = models.CharField(max_length=30)
    state = models.CharField(max_length=20, null=True)
    coverage = models.OneToOneField(Coverage, on_delete=models.CASCADE, null=True)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True)
    #document = models.FileField(upload_to='uploads/')

class PolicyDoc(models.Model):
    document = models.FileField(upload_to='uploads/')
