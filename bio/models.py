from django.db import models
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Bio(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bio'
    )
    bio = models.TextField(blank=True)
    cv = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage()
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bio for {self.owner.username}"