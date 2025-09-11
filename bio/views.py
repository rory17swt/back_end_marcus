from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Bio
from .serializers.common import BioSerializer


# Authenticated Client View for GET / PUT / PATCH / DELETE
class BioDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.bio
        except Bio.DoesNotExist:
            raise NotFound("You haven't created your bio yest")
    
# Authenticated Client View for POST
class CreateBioView(generics.CreateAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'bio'):
            raise PermissionDenied("You have already created you bio.")
        serializer.save(owner=user)

# Public View
class PublicBioView(generics.RetrieveAPIView):
    serializer_class = BioSerializer
    permission_classes = []

    def get_object(self):
        try:
            return Bio.objects.get(owner__id=3)
        except Bio.DoesNotExist:
            raise NotFound("Bio does not exist.")