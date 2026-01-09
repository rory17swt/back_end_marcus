from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from .models import Bio
from .serializers.common import BioSerializer


class CreateBioView(generics.CreateAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if hasattr(user, 'bio'):
            raise PermissionDenied("You have already created your bio.")

        self.perform_create(serializer, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, user):
        serializer.save(owner=user)


class BioDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.bio
        except Bio.DoesNotExist:
            raise NotFound("You haven't created your bio yet.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class PublicBioView(generics.RetrieveAPIView):
    serializer_class = BioSerializer
    permission_classes = []

    def get_object(self):
        try:
            return Bio.objects.get(owner__id=3)
        except Bio.DoesNotExist:
            raise NotFound("Bio does not exist.")
