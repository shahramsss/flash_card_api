from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .models import Todo
from datetime import date, timedelta
from .forms import TodoForm
from django.utils import timezone

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
        todo = get_object_or_404(Todo, id=todo_id,)
        return render(request, "todo/todo_confirm.html", {"todo": todo})

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id,)

        new_daily_todo = Todo.objects.create(
            title=todo.title,
            description=todo.description,
            due_date=date.today(),
            start_time = timezone.localtime().time(),
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
