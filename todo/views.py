from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Todo
from datetime import date, timedelta
from khayyam import JalaliDate

class TodoListView(View):
    def get(self, request):
        today = date.today()
        days = [today + timedelta(days=i) for i in range(14)]  # ۱۴ روز آینده

        # دیکشنری روزها و تسک‌ها
        days_dict = {}
        for d in days:
            days_dict[d] = Todo.objects.filter(due_date=d).order_by("due_time")

        return render(request, "todo/todo_list.html", {"days_dict": days_dict})

    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        due_time = request.POST.get("due_time")
        priority = request.POST.get("priority", "medium")

        if title:
            Todo.objects.create(
                title=title,
                description=description,
                due_date=due_date or None,
                due_time=due_time or None,
                priority=priority,
            )
        return redirect("todo:todo_list")


class TodoUpdateView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, "todo_edit.html", {"todo": todo})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.title = request.POST.get("title")
        todo.description = request.POST.get("description")
        todo.due_date = request.POST.get("due_date") or None
        todo.due_time = request.POST.get("due_time") or None
        todo.priority = request.POST.get("priority", "medium")
        todo.is_completed = bool(request.POST.get("is_completed"))
        todo.save()
        return redirect("todo_list")
