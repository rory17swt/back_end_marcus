from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Media
from .serializers.common import MediaSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils.cloudinary import handle_file_upload


class MediaListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    # Index
    def get(self, request):
        medias = Media.objects.all()
        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)

    # Create
    def post(self, request):
        # Don't use .copy() with files - use a regular dict instead
        data = {}
        
        # Copy regular fields
        for key, value in request.data.items():
            if key != 'image':
                data[key] = value
       
        # Handle image upload
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
    parser_classes = [MultiPartParser, FormParser]

    # Show
    def get(self, request, pk):
        media = get_object_or_404(Media, pk=pk)
        serializer = MediaSerializer(media)
        return Response(serializer.data)

    # Delete
    def delete(self, request, pk):
        media = get_object_or_404(Media, pk=pk)
        self.check_object_permissions(request, media)
        media.delete()
        return Response({"detail": "Media deleted"}, status=204)
