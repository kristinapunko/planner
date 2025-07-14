from django.urls import path
from . import views
from .views import Login, RegisterUser, Logout

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("", views.main_page, name='main'),
    path("addtask/", views.add_task, name="add task"),
    path("detail/<int:id>/", views.view_page, name='detail'),
    path('tasks/<int:id>/edit/', views.task_edit, name='task-edit'),
    path('tasks/<int:id>/delete/', views.task_delete, name='task-delete'),
    path('task/<int:id>/done/', views.mark_done, name='done'),
]