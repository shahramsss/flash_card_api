from django.shortcuts import render
from rest_framework.views import APIView
from .models import FlashCard
from .serializers import FlashCardSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from datetime import timedelta, date


class Home(APIView):
    def get(self, request):
        flash_cards = FlashCard.objects.all()
        serializer = FlashCardSerializer(flash_cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        word = request.data.get("word", "").strip()
        if not word:
            return Response(
                {"error": "فیلد 'word' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # بررسی وجود کلمه تکراری
        if FlashCard.objects.filter(word=word).exists():
            raise ValidationError("این کلمه قبلاً ثبت شده است.")
        serializer = FlashCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Word(APIView):
    def get_object(self, pk):
        """
        متدی برای دریافت یک فلش‌کارت با بررسی وجود
        """
        try:
            return FlashCard.objects.get(pk=pk)
        except FlashCard.DoesNotExist:
            raise NotFound(detail="این فلش‌کارت یافت نشد!", code=404)

    def get(self, request, pk):
        """
        دریافت اطلاعات یک فلش‌کارت بر اساس کلید اصلی
        """
        flash_card = self.get_object(pk)
        serializer = FlashCardSerializer(flash_card)
        return Response(data=serializer.data)

    def put(self, request, pk):
        """
        به‌روزرسانی یک فلش‌کارت
        """
        flash_card = self.get_object(pk)
        data = request.data

        # بررسی مقدار last_reply و افزایش نرخ
        last_reply = data.get("last_reply")
        rate = int(flash_card.rate)
        next_review_date = flash_card.next_review_date
        today = date.today()
        if (
            last_reply in ["True", "true", True]
            and rate < 8
            and next_review_date <= today
        ):

            data["rate"] = rate + 1
            data["next_review_date"] = date.today() + timedelta(days=1)

        # سریالایز و ذخیره داده‌ها
        serializer = FlashCardSerializer(flash_card, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # بازگرداندن خطاهای اعتبارسنجی
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flash_card = self.get_object(pk)  # دریافت فلش‌کارت
        flash_card.delete()  # حذف فلش‌کارت
        return Response(
            {"detail": "فلش‌کارت با موفقیت حذف شد!"}, status=status.HTTP_204_NO_CONTENT
        )
