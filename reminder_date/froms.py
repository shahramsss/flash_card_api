from django import forms
from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["title", "one", "two", "seven", "month", "year"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "عنوان یادآور را وارد کنید",
                }
            ),
            "one": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "two": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "seven": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "month": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "year": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "عنوان یادآور",
            "one": " روزاول",
            "two": "روز دوم",
            "seven": "روز هفتم",
            "month": "ماه",
            "year": "سال",
        }
