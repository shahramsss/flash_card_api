"""
URL configuration for flash_card project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *


app_name = "todo"
urlpatterns = [
    path("todos/", TodoListView.as_view(), name="todo_list"),
    path("todos/<int:todo_id>/", TodoDetailView.as_view(), name="todo_detail"),
    path("todo_daily_confirm/<int:todo_id>/", TodoDailyView.as_view(), name="todo_daily_confirm"),
    path("todo/delete/<int:todo_id>/",TodoDeleteView.as_view(),name="todo_delete"),
    path("summary/time/<int:todo_id>/", DailySummaryTimeView.as_view(), name="daily_summary_time"),


]
