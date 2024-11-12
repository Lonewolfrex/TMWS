from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProjectForm
from .models import Project, ProjectStep
from django.contrib.auth.forms import AuthenticationForm

def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

@login_required
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('project_list')

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('login')

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            # Create default steps for the new project
            default_steps = [
                {"name": "Scoping the work", "description": "Define the scope of the work."},
                {"name": "Determine threats", "description": "Identify potential threats."},
                {"name": "Determine Countermeasures for mitigation", "description": "Plan countermeasures."},
                {"name": "Assessing the Work", "description": "Evaluate the work done."},
            ]

            for step in default_steps:
                ProjectStep.objects.create(
                    project=project,
                    name=step["name"],
                    description=step["description"]
                )

            return redirect('project_detail', pk=project.pk)  # Redirect to project detail page
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)  # Get the project or return 404
    steps = project.steps.all()  # Get all steps related to this project
    return render(request, 'project_detail.html', {'project': project, 'steps': steps})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()  # Save the updated project
            return redirect('project_detail', pk=project.pk)  # Redirect to project detail page
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def toggle_step(request, step_id):
    step = get_object_or_404(ProjectStep, id=step_id)
    
    # Toggle the completion status
    step.is_complete = not step.is_complete
    step.save()
    
    return redirect('project_detail', pk=step.project.pk)