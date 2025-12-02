from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Production
from .serializers.production import ProductionSerializer


class ProductionListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """List all productions"""
        productions = Production.objects.all()
        serializer = ProductionSerializer(productions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new production"""
        serializer = ProductionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class ProductionDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        """Get a single production by slug"""
        production = get_object_or_404(Production, slug=slug)
        serializer = ProductionSerializer(production)
        return Response(serializer.data)

    def put(self, request, slug):
        """Update a production"""
        production = get_object_or_404(Production, slug=slug)
        serializer = ProductionSerializer(production, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        """Delete a production"""
        production = get_object_or_404(Production, slug=slug)
        production.delete()
        return Response({"detail": "Production deleted"}, status=204)