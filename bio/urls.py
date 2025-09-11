from django.urls import path
from .views import BioDetailUpdateView, CreateBioView, PublicBioView

urlpatterns = [
    path('bio/public/', PublicBioView.as_view()),
    path('bio/create/', CreateBioView.as_view()),
    path('bio/', BioDetailUpdateView.as_view())
]