from django import forms

class ReminderForm(forms.Form):
    title = forms.CharField(
        max_length=512,
        label="عنوان",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_day = forms.DateField(
        label="تاریخ شروع",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    one = forms.DateField(
        label="روز اول",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    two = forms.DateField(
        label="روز دوم",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    seven = forms.DateField(
        label="روز هفتم",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    month = forms.DateField(
        label="ماه",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    year = forms.DateField(
        label="سال",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
   
