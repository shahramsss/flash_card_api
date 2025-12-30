from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime


class Todo(models.Model):

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان")

    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    due_date = models.DateField(blank=True, null=True, verbose_name="تاریخ")

    start_time = models.TimeField(blank=True, null=True, verbose_name="ساعت شروع")

    end_time = models.TimeField(blank=True, null=True, verbose_name="ساعت پایان")

    is_completed = models.BooleanField(default=False, verbose_name="انجام شده")

    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="low", verbose_name="اولویت"
    )
    is_daily = models.BooleanField(
        default=False,
        verbose_name="کار روزانه"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        ordering = ["due_date", "start_time"]
        verbose_name = "وظیفه"
        verbose_name_plural = "وظایف"

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"

    def clean(self):
        # اعتبارسنجی ساعت شروع و پایان
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError(
                    {"end_time": "ساعت پایان باید بعد از ساعت شروع باشد"}
                )

        # اگر ساعت وارد شده، تاریخ باید وجود داشته باشد
        if (self.start_time or self.end_time) and not self.due_date:
            raise ValidationError({"due_date": "برای تعیین ساعت، تاریخ را وارد کنید"})

    def save(self, *args, **kwargs):
        # اجرای اعتبارسنجی قبل از ذخیره
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """مدت زمان انجام کار"""
        if self.start_time and self.end_time and self.due_date:
            start = datetime.combine(self.due_date, self.start_time)
            end = datetime.combine(self.due_date, self.end_time)
            return end - start
        return None
