from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers.tokens import CustomTokenSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer