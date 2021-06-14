from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crittercatcherapi.models import Request, Requestor, Category, category

class RequestSerializer(serializers.ModelSerializer):
    """JSON serializer for request
    Arguments:
        serializer type
    """
    class Meta:
        model = Request
        fields = ('id', 'title', 'location', 'description', 'date', 'requestor','image_url','is_complete', 'category',)
        depth = 1

class Requests(ViewSet):
    def create(self, request):
        requestor = Requestor.objects.get(user=request.auth.user)

        request = Request()
        
        request.title = request.data["title"]
        request.description = request.data["description"]
        request.location = request.data["location"]
        request.date = request.data["date"]
        request.requestor = requestor
        

        category = Category.objects.get(pk=request.data["categoryId"])
        request.Category = category

        try:

            request.save()
            serializer = RequestSerializer(request, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            
            request = Request.objects.get(pk=pk)
            serializer = RequestSerializer(request, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to request resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all request records from the database
        requests = Request.objects.all()

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