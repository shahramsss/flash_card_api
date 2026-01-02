from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    start_time = forms.TimeField(
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={
                "type": "time",
                "class": "form-control",
            },
        ),
    )

    end_time = forms.TimeField(
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={
                "type": "time",
                "class": "form-control",
            },
        ),
    )

    class Meta:
        model = Todo
        fields = [
            "title",
            "description",
            "due_date",
            "start_time",
            "end_time",
            "priority",
            "is_completed",
            "is_daily",
        ]
        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_daily": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"].required = True
