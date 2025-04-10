from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Task
from django.contrib import messages
from .forms import SignUpForm, TaskForm
from rest_framework import generics, permissions
from .serializers import TaskSerializer


# Create your views here.

# API view to handle task creation and listing
# This view will be used to create and list tasks via API

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(userid__username=self.request.user.username)

    def perform_create(self, serializer):
        serializer.save(userid=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(userid__username=self.request.user.username)
    
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('tasks')
           
          
    else:
        form = SignUpForm()
        messages.error(request, 'Registration failed. Please try again.')
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')



@login_required
def tasks(request):
    task_list = Task.objects.filter(userid=request.user)
    form = TaskForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.userid = request.user  
        task.save()
        return redirect('tasks')

    return render(request, 'tasks.html', {'tasks': task_list, 'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, userid__username=request.user.username)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, userid__username=request.user.username)
    task.delete()
    return redirect('tasks')

