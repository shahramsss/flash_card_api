from django.shortcuts import render
from rest_framework.views import APIView
from .models import FlashCard
from .serializers import FlashCardSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from khayyam import JalaliDate
from datetime import datetime 



class Home(APIView):
    def get(self, request):
        flash_cards = FlashCard.objects.all()
        serializer = FlashCardSerializer(flash_cards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FlashCardSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Word(APIView):
    
    def get(self, request , pk):
        try:
            flashcard = get_object_or_404(FlashCard, pk=pk)  # استفاده از get_object_or_404
        except:
            raise NotFound(detail="این مورد وجود ندارد!", code=404)

        serializer = FlashCardSerializer(flashcard)
        return Response(data=serializer.data)
    
    def update(self, request , pk ):
        pass

    def delete(self, request , pk ):
        pass
