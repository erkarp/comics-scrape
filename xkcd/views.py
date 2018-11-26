from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from xkcd.models import Comic


def xkcds(request):
    stored_comics = Comic.objects.order_by('-number')
    paginator = Paginator(stored_comics, 20)
    page = request.GET.get('page', 1)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        return JsonResponse({})

    comics_json = []
    for comic in data:
        comics_json.append({
            'xkcd': comic.number,
            'date': comic.published,
            'name': comic.display_name,
            'file': comic.img_filename,
        })

    return JsonResponse({'comics': comics_json, 'page': page}, safe=False)
