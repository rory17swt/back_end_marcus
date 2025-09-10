from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Event
from .serializers.common import EventSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils.cloudinary import handle_file_upload

class EventListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    # Index
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    # Create
    def post(self, request):
        data = handle_file_upload(request, 'image', folder='marcus_uploads')
        data['owner'] = request.user.id
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class EventDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    # Show
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    # Update
    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(request, event)
        data = handle_file_upload(request, 'image', folder='marcus_uploads')
        serializer = EventSerializer(event, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(request, event)
        event.delete()
        return Response({ "detail": "Event deleted" }, status=204)