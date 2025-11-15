from django.shortcuts import render
from .models import Reminder
from django.views import View


class ReminderHomeView(View):
    def get(self , request):
        reminders = Reminder.objects.all().order_by('-start_day')
        return render(request , "reminder_date/home.html" , {"reminders":reminders})