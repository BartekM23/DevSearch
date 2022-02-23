from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from users.models import Skill, Profile


def paginate_profiles(request, all_profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(all_profiles, results)
    try:
        all_profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        all_profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        all_profiles = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, all_profiles


def search_profiles(request):
    text = ''
    if request.GET.get('text'):
        text = request.GET.get('text')

    skills = Skill.objects.filter(name__icontains=text)
    all_profiles = Profile.objects.distinct().filter(
        Q(name__icontains=text) |
        Q(short_intro__icontains=text) |
        Q(skill__in=skills))
    return all_profiles, text
