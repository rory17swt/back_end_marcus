from django.db import models
from django.conf import settings


class Bio(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bio'
    )
    bio = models.TextField(blank=True)
    cv = models.URLField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bio for {self.owner.username}"