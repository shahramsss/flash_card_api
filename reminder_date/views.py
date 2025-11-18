from django.shortcuts import render, get_object_or_404
from .models import Reminder
from django.views import View
from datetime import timedelta
from .froms import ReminderForm


class ReminderHomeView(View):
    def get(self, request):
        reminders = Reminder.objects.all().order_by("-start_day")
        context = []
        for r in reminders:
            context.append(
                {
                    "title": r.title,
                    "start_day": r.start_day,
                    "one_date": r.start_day + timedelta(days=1),
                    "two_date": r.start_day + timedelta(days=3),
                    "seven_date": r.start_day + timedelta(days=10),
                    "month_date": r.start_day + timedelta(days=40),
                    "year_date": r.start_day + timedelta(days=405),
                    "one": r.one,
                    "two": r.two,
                    "seven": r.seven,
                    "month": r.month,
                    "year": r.year,
                }
            )

        return render(request, "reminder_date/home.html", {"reminders": context})


class ReminderDetailsView(View):
    form_class = ReminderForm

    def get(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk)
        form = self.form_class(instance=reminder)   
        return render(
            request,
            "reminder_date/reminderdetails.html",
            {"reminder": reminder, "form": form},
        )
