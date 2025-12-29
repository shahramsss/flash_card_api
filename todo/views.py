from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .models import Todo
from datetime import date, timedelta
from .forms import TodoForm


class TodoListView(View):
    def get(self, request):
        today = date.today()

        # ۱۴ روز آینده (شامل امروز)
        days = [today + timedelta(days=i) for i in range(14)]

        # دیکشنری روزها و کارها
        days_dict = {
            day: Todo.objects.filter(due_date=day).order_by("due_time") for day in days
        }

        # کارهای آینده (بعد از امروز)
        future_todos = Todo.objects.filter(
            due_date__gt=today, is_completed=False
        ).order_by("due_date", "due_time")

        return render(
            request,
            "todo/todo_list.html",
            {
                "days_dict": days_dict,
                "future_todos": future_todos,
            },
        )

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
    def get(self, request, todo_id):
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
        return redirect(
            "todo:todo_list",
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


# class TodoFuturView(view):
#     def get(self , request):
#         today = date.today()
#         todo = get_object_or_404(Todo, pk=todo_id, due_date__gte=today)
#         return render()
