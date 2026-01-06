from django import forms
from .models import FlashCard, FlashLeitner


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ["word", "meaning", "example"]

        widgets = {
            "word": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the word",
                }
            ),
            "meaning": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the meaning",
                }
            ),
            "example": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter an example (optional)",
                }
            ),
            "rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 5,
                    "placeholder": "Rate (0-5)",
                }
            ),
            "last_reply": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "next_review_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }


class FlashLeitnerForm(forms.ModelForm):
    class Meta:
        model = FlashLeitner
        fields = [
            "word",
            "meaning",
            "example",
        ]

        widgets = {
            "word": forms.TextInput(attrs={"class": "form-control"}),
            "meaning": forms.TextInput(attrs={"class": "form-control"}),
            "example": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "last_reply": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "next_review_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "start_day": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
