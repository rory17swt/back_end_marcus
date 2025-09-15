from rest_framework import serializers
from ..models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def validate(self, data):
            image = data.get('image')
            youtube_url = data.get('youtube_url')

            if not image and not youtube_url:
                raise serializers.ValidationError("You must provide an image, YouTube URL or both.")
            return data