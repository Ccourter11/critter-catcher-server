from django.db import models
from crittercatcherapi.models.requestor import Requestor
from crittercatcherapi.models.request import Request

class Review(models.Model):

    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    review = models.CharField(max_length=250)