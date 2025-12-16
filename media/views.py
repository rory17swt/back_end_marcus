from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404

from .models import Media
from .serializers.common import MediaSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils.cloudinary import handle_file_upload


class MediaListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        List media items with optional production filtering.
        
        Query params:
            - production: filter by production slug
        """
        medias = Media.objects.select_related('production').all()
        
        # Filter by production slug
        production_slug = request.query_params.get('production')
        if production_slug:
            medias = medias.filter(production__slug=production_slug)
        
        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {}
        
        for key, value in request.data.items():
            if key != 'image':
                data[key] = value
       
        if 'image' in request.FILES:
            image_upload_data = handle_file_upload(request, 'image', folder='marcus_uploads')
            data['image'] = image_upload_data.get('image')

        data['owner'] = request.user.id

        serializer = MediaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class MediaDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        media = get_object_or_404(Media.objects.select_related('production'), pk=pk)
        serializer = MediaSerializer(media)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a media item (e.g., change production tag)"""
        media = get_object_or_404(Media, pk=pk)
        self.check_object_permissions(request, media)
        
        data = {}
        for key, value in request.data.items():
            if key != 'image':
                data[key] = value
        
        if 'image' in request.FILES:
            image_upload_data = handle_file_upload(request, 'image', folder='marcus_uploads')
            data['image'] = image_upload_data.get('image')
        
        serializer = MediaSerializer(media, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        media = get_object_or_404(Media, pk=pk)
        self.check_object_permissions(request, media)
        media.delete()
        return Response({"detail": "Media deleted"}, status=204)