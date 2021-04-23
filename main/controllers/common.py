from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

from main.services.ItemRepository import ItemRepository


def common(request):
    """Общий контроллер."""

    repo = ItemRepository()
    if request.method == 'GET':
        data = {}
        if request.GET:
            result = repo.get_item(**request.GET)
        else:
            result = repo.get_item()

        data['pos'] = result['pos']

        if 'HTTP_ACCEPT' in request.META \
                and request.META['HTTP_ACCEPT'] == 'application/json':
            data['item'] = result['item'].to_dict()
            return JsonResponse(data)
        else:
            data = repo.get_category_data()
            data['item'] = result['item']
            return render(request, 'index.html', data)
    else:
        return HttpResponseNotAllowed(['GET'])


def build_http_error_response(request, data):
    """Строит ответ сервера на HTTP-ошибку."""

    if 'HTTP_ACCEPT' in request.META \
            and request.META['HTTP_ACCEPT'] == 'application/json':
        return JsonResponse(data, status=data['code'])
    else:
        return render(request, 'http-error.html', data, status=data['code'])


def http400(request, exception):
    data = {
        'code': 400,
        'text': 'Плохой запрос'
    }
    return build_http_error_response(request, data)


def http403(request, exception):
    data = {
        'code': 403,
        'text': 'Доступ запрещён'
    }
    return build_http_error_response(request, data)


def http404(request, exception):
    data = {
        'code': 404,
        'text': 'Страница не&nbsp;найдена'
    }
    return build_http_error_response(request, data)


def http500(request):
    data = {
        'code': 500,
        'text': 'Ошибка сервера'
    }
    return build_http_error_response(request, data)
