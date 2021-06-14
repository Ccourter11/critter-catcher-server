from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crittercatcherapi.models import Category, category


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categeory types
    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')


class Categories(ViewSet):
    """Critter catcher categories"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single animal category
        Returns:
            Response -- JSON serialized animal category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to get all animal category
        Returns:
            Response -- JSON serialized list of game types
        """
        category = Category.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            category, many=True, context={'request': request})
        return Response(serializer.data)        