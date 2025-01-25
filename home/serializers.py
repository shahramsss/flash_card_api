from .models import FlashCard
from rest_framework import serializers

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = "__all__"
        
