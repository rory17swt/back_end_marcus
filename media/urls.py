from django.urls import path
from .views import MediaListCreate, MediaDetailView
from .views_production import ProductionListCreate, ProductionDetailView

urlpatterns = [
    path('media/', MediaListCreate.as_view()),
    path('media/<int:pk>/', MediaDetailView.as_view()),

    # Production endpoints
    path('productions/', ProductionListCreate.as_view()),
    path('productions/<slug:slug>/', ProductionDetailView.as_view())
]