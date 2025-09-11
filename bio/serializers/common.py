from rest_framework import serializers
from ..models import Bio

class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ['bio', 'cv', 'updated_at']
        read_only_fields = ['updated_at']

