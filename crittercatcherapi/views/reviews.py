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

    def list(self, request):
        """Handle GET requests to get all reviews 
        Returns:
            Response -- JSON serialized list of game types
        """
        review = Review.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ReviewSerializer(
            review, many=True, context={'request': request})
        return Response(serializer.data) 

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     


    def update(self, request, pk=None):
        """Handle PnUT requests for a request
        Returns:
            Response -- Empty body with 204 status code
        """
        
        requestor = Requestor.objects.get(user=request.auth.user)
        
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        review = Review.objects.get(pk=pk)
        review.request = Request.objects.get(pk=request.data["requestId"])
        review.requestor = requestor
        review.review = request.data["review"]
        review.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)          