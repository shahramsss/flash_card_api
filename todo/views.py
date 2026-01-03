from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .models import Todo
from datetime import date, timedelta, datetime
from .forms import TodoForm
from django.utils import timezone
from collections import defaultdict
from django.db.models import F, ExpressionWrapper, DurationField, Sum, Count
from django.db.models.functions import ExtractWeek, ExtractMonth
from collections import defaultdict
import jdatetime


class TodoListView(View):
    form_class = TodoForm

    def get(self, request):
        today = date.today()
        form = self.form_class()

        # ۱۴ روز آینده (شامل امروز)
        days = [today + timedelta(days=i) for i in range(14)]

        # دیکشنری روزها و کارها
        days_dict = {
            day: Todo.objects.filter(due_date=day).order_by("start_time")
            for day in days
        }

        # کارهای آینده (بعد از امروز)
        future_todos = Todo.objects.filter(
            due_date__gt=today, is_completed=False
        ).order_by("due_date", "start_time")
        daily_todos = Todo.objects.filter(
            is_daily=True,
        )
        past_todos = Todo.objects.filter(
            due_date__lt=today,
            is_completed=False,
        ).order_by("-due_date")

        #  sum totla time daily

        todos_totla_time = Todo.objects.filter

        return render(
            request,
            "todo/todo_list.html",
            {
                "days_dict": days_dict,
                "future_todos": future_todos,
                "form": form,
                "daily_todos": daily_todos,
                "past_todos": past_todos,
            },
        )

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect("todo:todo_list")

        # اگر فرم نامعتبر بود، همون صفحه با خطا برگرده
        today = date.today()
        days = [today + timedelta(days=i) for i in range(14)]

        days_dict = {
            day: Todo.objects.filter(due_date=day).order_by("start_time")
            for day in days
        }

        future_todos = Todo.objects.filter(
            due_date__gt=today, is_completed=False
        ).order_by("due_date", "start_time")

        return render(
            request,
            "todo/todo_list.html",
            {
                "days_dict": days_dict,
                "future_todos": future_todos,
                "form": form,
            },
        )


class TodoDetailView(View):
    from_class = TodoForm

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        form = self.from_class(instance=todo)
        return render(request, "todo/todo_detail.html", {"todo": todo, "form": form})

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, pk=todo_id)
        form = self.from_class(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect(
                "todo:todo_list",
            )
        return render(request, "todo/todo_detail.html", {"todo": todo, "form": form})


class TodoDailyView(View):

    def get(self, request, todo_id):
        todo = get_object_or_404(
            Todo,
            id=todo_id,
        )
        return render(request, "todo/todo_confirm.html", {"todo": todo})

    def post(self, request, todo_id):
        todo = get_object_or_404(
            Todo,
            id=todo_id,
        )

        new_daily_todo = Todo.objects.create(
            title=todo.title,
            description=todo.description,
            due_date=date.today(),
            start_time=timezone.localtime().time(),
            priority=todo.priority,
            is_daily=False,
            is_completed=False,
        )

        return redirect("todo:todo_detail", new_daily_todo.id)


class TodoDeleteView(View):
    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        return render(request, "todo/todo_delete_confirm.html", {"todo": todo})

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        todo.delete()
        return redirect("todo:todo_list")



class SummaryTimeView(View):
    """
    نمایش جمع زمان صرف شده روی یک کار روزانه مشخص
    - گروه‌بندی بر اساس هفته و ماه
    """

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)

        todos = Todo.objects.filter(
            title=todo.title,
            start_time__isnull=False,
            end_time__isnull=False,
            due_date__isnull=False,
            is_completed=True,
        )

        todo_times = {"weeks": {}, "months": {}}

        for t in todos:
            # miladi date 
            # iso = t.due_date.isocalendar()
            # week_key = f"{iso.year}-{iso.week}"
            # month_key = f"{t.due_date.year}-{t.due_date.month}"

            # jalali date 
            j_date = jdatetime.date.fromgregorian(date=t.due_date)
            jalali_year = j_date.year
            month_key = j_date.month
            start_of_year = jdatetime.date(jalali_year, 1, 1)
            week_key = ((j_date - start_of_year).days // 7) + 1

            start = datetime.combine(t.due_date, t.start_time)
            end = datetime.combine(t.due_date, t.end_time)
            duration = end - start  # timedelta

            # ---- weekly ----
            if week_key not in todo_times["weeks"]:
                todo_times["weeks"][week_key] = {
                    "title": t.title,
                    "duration": duration,
                }
            else:
                todo_times["weeks"][week_key]["duration"] += duration

            # ---- monthly ----
            if month_key not in todo_times["months"]:
                todo_times["months"][month_key] = {
                    "title": t.title,
                    "duration": duration,
                }
            else:
                todo_times["months"][month_key]["duration"] += duration

        return render(
            request,
            "todo/daily_summary_time.html",
            {"todo_times": todo_times, "todo": todo},
        )
