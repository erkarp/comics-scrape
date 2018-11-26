from django.http import JsonResponse
from xkcd.models import Comic


def xkcds(request):
    data = []
    for comic in Comic.objects.order_by('-number'):
        data.append({
            'xkcd': comic.number,
            'date': comic.published,
            'name': comic.display_name,
            'file': comic.img_filename,
        })

    return JsonResponse(data, safe=False)
