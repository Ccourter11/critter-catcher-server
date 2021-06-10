from crittercatcherapi.models.requestor import Requestor
from crittercatcherapi.models.category import Category
from django.db import models


class Request(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=50)
    date = models.DateTimeField(max_length=50)
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=50)
    is_complete = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


