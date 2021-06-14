from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crittercatcherapi.models import Requestor, Review, Request


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review
    Arguments:
        serializer type
    """
    class Meta:
        model = Review
        fields = ('id', 'requestor', 'request','review',)
        depth = 1

class Reviews(ViewSet):
    def create(self, request):
        requestor = Requestor.objects.get(user=request.auth.user)

        review = Review()
        
        review.requestor = requestor
        review.request = Request.objects.get(pk=request.data["requestId"])
        review.review = request.data["review"]

        try:

            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)    

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)    

    def retrieve(self, request, pk=None):
        """Handle GET requests for single review
        Returns:
            Response -- JSON serialized review instance
        """
        try:
            
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)        