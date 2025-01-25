from django.shortcuts import render
from rest_framework.views import APIView
from .models import FlashCard
from .serializers import FlashCardSerializer
from rest_framework.response import Response


class Home(APIView):
    def get(self, request):
        flash_cards = FlashCard.objects.all()
        serializer = FlashCardSerializer(flash_cards, many=True)
        return Response(serializer.data)
