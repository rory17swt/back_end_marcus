from django.urls import path
from .views import submit_contact_form, get_csrf_token

urlpatterns = [
    path('contact/submit/', submit_contact_form),
    path('contact/csrf/', get_csrf_token),
]
