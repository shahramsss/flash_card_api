from django.shortcuts import render
from rest_framework.views import APIView
from .models import FlashCard
from .serializers import FlashCardSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from khayyam import JalaliDate
from datetime import datetime , date



class Home(APIView):
    def get(self, request):
        flash_cards = FlashCard.objects.all()
        serializer = FlashCardSerializer(flash_cards, many=True)
        for item in serializer.data:
            try:
                next_review_date = item['next_review_date']
                if next_review_date:
                    if isinstance(next_review_date, str):
                        next_review_date = datetime.strptime(next_review_date, "%Y-%m-%d").date()
                        item['j_next_review_date'] = JalaliDate(next_review_date).strftime("%A, %d %B, %Y")
            except Exception as e:
                print(f"Error converting next_review_date: {e}")
        return Response(serializer.data)


class Word(APIView):
    
    def get(self, request , pk):
        try:
            flashcard = get_object_or_404(FlashCard, pk=pk)  # استفاده از get_object_or_404
        except:
            raise NotFound(detail="این مورد وجود ندارد!", code=404)

        serializer = FlashCardSerializer(flashcard)
        data = serializer.data
        data['j_next_review_date'] = JalaliDate(flashcard.next_review_date).strftime("%A,%d %B, %Y")
        return Response(data=data)
    
    def post(self, request):
        serializer = FlashCardSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request , pk ):
        pass

    def delete(self, request , pk ):
        pass
