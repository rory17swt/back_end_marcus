from django.urls import path
from .views import MediaListCreate, MediaDetailView

urlpatterns = [
    path('media/', MediaListCreate.as_view()),
    path('media/<int:pk>/', MediaDetailView.as_view())
]