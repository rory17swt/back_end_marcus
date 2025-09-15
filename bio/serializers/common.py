from rest_framework import serializers
from ..models import Bio

class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ['id', 'bio', 'cv', 'updated_at']
        read_only_fields = ['updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep
