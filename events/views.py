from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Event
from .serializers.common import EventSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils.cloudinary import handle_file_upload