from rest_framework import serializers
from ..models import Production


class ProductionSerializer(serializers.ModelSerializer):
    media_count = serializers.SerializerMethodField()

    class Meta:
        model = Production
        fields = ['id', 'name', 'slug', 'year', 'media_count']
        read_only_fields = ['slug']

    def get_media_count(self, obj):
        return obj.media_items.count()