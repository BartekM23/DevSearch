from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectFrom, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import search_projects, paginate_projects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


# Create your views here.

def projects(request):
    all_projects, text = search_projects(request)

    custom_range, all_projects = paginate_projects(request, all_projects, 6)

    context = {'custom_range': custom_range, 'projects': all_projects, 'search_query': text}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.vote_count()
        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=project_obj.id)

    context = {'project': project_obj, 'form': form}
    return render(request, 'projects/project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectFrom()
    if request.method == "POST":
        new_tags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectFrom(request.POST, request.FILES)
        if form.is_valid():
            this_project = form.save(commit=False)
            this_project.owner = profile
            this_project.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectFrom(instance=project)
    if request.method == "POST":
        new_tags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectFrom(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')

    context = {'form': form, 'project':project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project_to_delete = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project_to_delete.delete()
        return redirect('projects')
    context = {'object': project_to_delete}
    return render(request, 'delete_object.html', context)
