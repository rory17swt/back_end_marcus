from django.db import models
from django.conf import settings

# Create your models here.
class Media(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='media'
    )
    image = models.CharField(max_length=500)
    youtube_url = models.URLField(blank=True, null=True, help_text="Paste the full YouTube URL")
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