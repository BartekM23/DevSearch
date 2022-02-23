from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from projects.models import Tag, Project


def paginate_projects(request, all_projects, results):
    page = request.GET.get('page')
    paginator = Paginator(all_projects, results)
    try:
        all_projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        all_projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        all_projects = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, all_projects


def search_projects(request):
    text = ''
    if request.GET.get('text'):
        text = request.GET.get('text')

    tags = Tag.objects.filter(name__icontains=text)

    all_projects = Project.objects.distinct().filter(
        Q(title__icontains=text) |
        Q(description__icontains=text) |
        Q(owner__name__icontains=text) |
        Q(tags__in=tags)
    )
    return all_projects, text
