from django.db import models
from .choices import ISSUE_STATUS

class Issue(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False)
    message = models.CharField(max_length=1000, blank=False, null=False)
    status = models.CharField(max_length=10, choices=ISSUE_STATUS, blank=False, null=False)
    priority = models.IntegerField(default=0)
