from django.db import models
from django.contrib.auth.models import User

class TransportRequest(models.Model):
    # field choices
    asset_choices = (
        ("LAPTOP", "LAPTOP"),
        ("TRAVEL_BAG", "TRAVEL_BAG"),
        ("PACKAGE", "PACKAGE")
    )

    senstivity_choices = (
        ("HIGHLY_SENSITIVE","HIGHLY_SENSITIVE"),
        ("SENSITIVE","SENSITIVE"),
        ("NORMAL","NORMAL")
    )

    status_choices = (
        ('PENDING','PENDING'),
        ('EXPIRED','EXPIRED')
    )

    # database fields
    source = models.CharField(max_length=40, null=False, blank=False)
    destination = models.CharField(max_length=40, null=False, blank=False)
    date_and_time = models.DateTimeField(null=False)
    flexible_timings = models.BooleanField(default=False)
    no_of_assets = models.IntegerField(null=False)
    asset_types = models.CharField(max_length=10, choices=asset_choices, null=False)
    asset_senstivity = models.CharField(max_length=20, choices=senstivity_choices, null=False)
    requested_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, null=False, choices=status_choices, default='PENDING')


class RiderTravelInfo(models.Model):
    # field choices
    medium_choices = (
        ("BUS", "BUS"),
        ("CAR", "CAR"),
        ("TRAIN", "TRAIN")
    )

    status_choices = (
        ('APPLIED','APPLIED'),
        ('NOT_APPLIED','NOT_APPLIED')
    )

    # database fields
    source = models.CharField(max_length=40, null=False, blank=False)
    destination = models.CharField(max_length=40, null=False, blank=False)
    date_and_time = models.DateTimeField(null=False)
    flexible_timings = models.BooleanField(default=False)
    no_of_assets = models.IntegerField(null=False)
    travel_medium = models.CharField(max_length=10, choices=medium_choices, null=False)
    uploaded_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=False, choices=status_choices, default='NOT_APPLIED')

class MatchedAssets(models.Model):
    # database fields
    request = models.ForeignKey(to=TransportRequest, on_delete=models.CASCADE)
    rider = models.ForeignKey(to=RiderTravelInfo, on_delete=models.SET_NULL, null=True)
