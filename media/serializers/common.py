from rest_framework import serializers
from ..models import Media


class MediaSerializer(serializers.ModelSerializer):
    production_name = serializers.CharField(source='production.name', read_only=True)
    production_slug = serializers.CharField(source='production.slug', read_only=True)
    youtube_embed_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            'id', 
            'owner', 
            'image', 
            'youtube_url', 
            'youtube_embed_url',
            'production',
            'production_name',
            'production_slug',
            'created_at'
        ]

    def get_youtube_embed_url(self, obj):
        return obj.get_youtube_embed_url()

    def validate(self, data):
        image = data.get('image')
        youtube_url = data.get('youtube_url')

        if not image and not youtube_url:
            raise serializers.ValidationError("You must provide an image, YouTube URL or both.")
        return data