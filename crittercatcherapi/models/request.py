from crittercatcherapi.models.requestor import Requestor
from django.db import models


class Request(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=50)
    date = models.DateTimeField(max_length=50)
    requestor = models.ForeignKey("Requestor", on_delete=models)
    image_url = models.CharField(max_length=50)
    is_complete = models.BooleanField()

#     title varchar
#   description varchar
#   location varchar
#   date datetime
#   requestorId int
#   imageUrl varchar
#   categoryId int
#   is_complete boolean

