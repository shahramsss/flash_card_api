from .models import FlashCard
from rest_framework import serializers
from khayyam import JalaliDate


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = "__all__"
        
    def get_created_at_jalali(self, obj):
        if obj.created_at:
            return JalaliDate(obj.created_at).strftime('%Y/%m/%d')
        return None

    def get_next_review_date_jalali(self, obj):
        if obj.next_review_date:
            return JalaliDate(obj.next_review_date).strftime('%Y/%m/%d')
        return None