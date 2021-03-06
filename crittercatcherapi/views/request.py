from crittercatcherapi.models.review import Review
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crittercatcherapi.models import Request, Requestor, Category, Review, requestor
from django.contrib.auth.models import User
from django.conf import settings
import cloudinary

class RequestSerializer(serializers.ModelSerializer):
    """JSON serializer for request
    Arguments:
        serializer type
    """
    class Meta:
        model = Request
        fields = ('id', 'title', 'location', 'description', 'date', 'requestor','image_url','is_complete', 'category',)
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', )

class RequestorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Requestor
        fields = ('id', 'bio','user',)
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    requestor = RequestorSerializer(many=False)
    class Meta:
        model = Review
        fields = ('id', 'review', 'request', 'requestor')        

class SingleRequestSerializer(serializers.ModelSerializer):
    """JSON serializer for request
    Arguments:
        serializer type
    """
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Request
        fields = ('id', 'title', 'location', 'description', 'date', 'requestor','image_url','is_complete', 'category','reviews',)
        # depth = 1




class Requests(ViewSet):
    cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'])

    def create(self, request):
        requestor = Requestor.objects.get(user=request.auth.user)

        new_request = Request()
        
        new_request.title = request.data["title"]
        new_request.description = request.data["description"]
        new_request.location = request.data["location"]
        new_request.date = request.data["date"]
        # if request.data["image_url"] !="":
        #     new_request.image_url = cloudinary.uploader.upload(request.data["image_url"])['url']
        new_request.image_url = cloudinary.uploader.upload(request.data['image_url'])['url']
        # new_request.is_complete = request.data["is_complete"]
        new_request.requestor = requestor
        

        category = Category.objects.get(pk=request.data["categoryId"])
        new_request.category = category

        try:

            new_request.save()
            serializer = RequestSerializer(new_request, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            reviews = Review.objects.filter(request=pk)
            request = Request.objects.get(pk=pk)
            request.reviews = reviews
            serializer = SingleRequestSerializer(request, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to request resource
        Returns:
            Response -- JSON serialized list of games
        """
        crittercatcher_user = Requestor.objects.get(user=request.auth.user)
        # Get all request records from the database
        requests = Request.objects.filter(requestor=crittercatcher_user)

        # Support filtering requests by category
        #    http://localhost:8000/request?category=1
        #
        # That URL will retrieve all small request
        category = self.request.query_params.get('category', None)
        if category is not None:
            requests = requests.filter(category__id=category)

        serializer = RequestSerializer(
            requests, many=True, context={'request': request})
        return Response(serializer.data)  

    def update(self, request, pk=None):
        """Handle PnUT requests for a request
        Returns:
            Response -- Empty body with 204 status code
        """
        requestor = Requestor.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        new_request = Request.objects.get(pk=pk)
        new_request.title = request.data["title"]
        new_request.description = request.data["description"]
        new_request.location = request.data["location"]
        new_request.date = request.data["date"]
        if request.data["image_url"] !="":
            new_request.image_url = cloudinary.uploader.upload(request.data['image_url'])['url']   
        new_request.requestor = requestor

        category = Category.objects.get(pk=request.data["categoryId"])
        new_request.category = category
        new_request.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)     

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            request = Request.objects.get(pk=pk)
            request.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Request.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                     