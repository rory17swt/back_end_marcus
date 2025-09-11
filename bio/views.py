from rest_framework import generics, permissions
from .models import Bio
from .serializers.common import BioSerializer


# Authenticated Client View for GET / PUT / PATCH / DELETE
class BioDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Bio.objects.get(owner=self.request.user)
    
# Authenticated Client View for POST
class CreateBioView(generics.CreateAPIView):
    serializer_class = BioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perfrom_create(self, serializer):
        serializer.save(owner=self.request.user)

# Public View
class PublicBioView(generics.RetrieveAPIView):
    serializer_class = BioSerializer
    permission_classes = []

    def get_object(self):
        return Bio.objects.get(owner__id=2)