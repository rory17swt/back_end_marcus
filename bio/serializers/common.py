from rest_framework import serializers
from ..models import Bio
import os

class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ['id', 'bio', 'cv', 'updated_at']
        read_only_fields = ['updated_at']

    def validate_cv(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.pdf':
            raise serializers.ValidationError("Only PDF files are allowed.")
        
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size must be under 5MB.")
        
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if instance.cv and request:
            rep['cv'] = request.build_absolute_uri(instance.cv.url)
        return rep