from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "title",
            "description",
            "due_date",
            "due_time",
            "priority",
            "is_completed",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "due_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
