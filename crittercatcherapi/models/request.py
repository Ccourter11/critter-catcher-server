from django.db import models


class Request(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=50)
    date = models.DateField()
    requestor = models.ForeignKey("Requestor", on_delete=models.CASCADE)
    image_url = models.URLField(null=True)
    is_complete = models.BooleanField(null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


