from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Production(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-year', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Production.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        if self.year:
            return f"{self.name} ({self.year})"
        return self.name


class Media(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='media'
    )
    image = models.CharField(max_length=500, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="Paste the full YouTube URL")
    production = models.ForeignKey(
        Production,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='media_items'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_youtube_embed_url(self):
        if self.youtube_url:
            if "watch?v=" in self.youtube_url:
                video_id = self.youtube_url.split("watch?v=")[-1].split("&")[0]
                return f"https://www.youtube.com/embed/{video_id}"
            elif "youtu.be/" in self.youtube_url:
                video_id = self.youtube_url.split("youtu.be/")[-1].split("?")[0]
                return f"https://www.youtube.com/embed/{video_id}"
        return None