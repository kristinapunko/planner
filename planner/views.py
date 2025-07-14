from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from .forms import RegisterUserForm
from django.contrib.auth import authenticate, login
from .models import Task
from .forms import TaskForm
from django.utils.timezone import now, localdate

class Login(LoginView):
    template_name = "users/accounts/login.html"

    def get_success_url(self):
        return '/'

class Logout(LogoutView):
    next_page = "/"

class RegisterUser(FormView):
    template_name = "users/accounts/register.html"
    form_class = RegisterUserForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response({'form': form})


def main_page(request):
    if not request.user.is_authenticated:
        return render(request, 'profile/profile.html', {'tasks': Task.objects.none()})

    tasks = Task.objects.filter(user=request.user)
    today = localdate()

    show_all = request.GET.get('show_all') == 'true'
    has_filters = any(request.GET.get(param) for param in 
                      ['status', 'priority', 'category', 'start_date', 'end_date', 'title', 'sort_by_date'])

    if not show_all and not has_filters:
        tasks = tasks.filter(
            done=False
        ).exclude(
            end_time__lt=today, no_deadline=False
        ).order_by(
            'no_deadline', 'end_time'
        )

    elif show_all:
        tasks = Task.objects.filter(user=request.user)

    else:
        if request.GET.get('title'):
            tasks = tasks.filter(title=request.GET.get('title'))

        status = request.GET.get('status')
        if status == 'done':
            tasks = tasks.filter(done=True)
        elif status == 'not_done':
            tasks = tasks.filter(done=False)
        elif status == 'overdue':
            tasks = tasks.filter(done=False, end_timee__lt=now())  

        if request.GET.get('priority'):
            tasks = tasks.filter(priority=request.GET.get('priority'))

        if request.GET.get('category'):
            tasks = tasks.filter(category=request.GET.get('category'))

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            tasks = tasks.filter(start_time_date=start_date)
        if end_date:
            tasks = tasks.filter(end_time_date=end_date)

        sort_by = request.GET.get('sort_by_date')
        if sort_by == 'asc':
            tasks = tasks.order_by('end_time')
        elif sort_by == 'desc':
            tasks = tasks.order_by('-end_time')

    context = {
        'tasks': tasks,
        'show_all': show_all,
        'now': now(),
        'categories': Task.objects.values_list('category', flat=True).distinct(),
        'current_filters': {k: v for k, v in request.GET.items() if k != 'show_all'},
        'title_query': request.GET.get('title', ''),
        'status_filter': request.GET.get('status', ''),
        'priority_filter': request.GET.get('priority', ''),
        'category_filter': request.GET.get('category', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'sort_by_date': request.GET.get('sort_by_date', '')
    }

    return render(request, 'profile/profile.html', context)

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        start_time = request.POST.get('start_time') or None
        end_time = request.POST.get('end_time') or None
        no_deadline = 'no_deadline' in request.POST
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')

        Task.objects.create(
            user=request.user,
            title=title,
            start_time=start_time,
            end_time=end_time,
            no_deadline=no_deadline,
            description=description,
            priority=priority,
            category=category,
        )
        return redirect("main")
    
    return render(request, "profile/add_task.html")


def view_page(request, id):
    task = Task.objects.get(id=id)
    return render(request, "profile/view_page.html", {'task':task})

def task_edit(request, id):
    task = Task.objects.get(id=id)
      
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'profile/task_edit.html', {'form': form, 'task': task})


def task_delete(request, id):
    task = Task.objects.filter(id=id)
    task.delete()
    return redirect('main')

def mark_done(request, id):
    task = Task.objects.get(id=id)
    task.done = True 
    task.save()
    return redirect('main')
