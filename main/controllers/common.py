from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

from main.services.ItemRepository import ItemRepository


def common(request):
    """Общий контроллер."""

    repo = ItemRepository()
    if request.method == 'GET':
        data = {}
        if request.GET:
            item = repo.get_item(**request.GET)
        else:
            item = repo.get_item()

        if 'HTTP_ACCEPT' in request.META \
                and request.META['HTTP_ACCEPT'] == 'application/json':
            item = item.to_dict()
            data['item'] = item
            return JsonResponse(data)
        else:
            data = repo.get_category_data()
            data['item'] = item
            return render(request, 'index.html', data)
    else:
        return HttpResponseNotAllowed(['GET'])
