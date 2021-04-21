from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
import logging

from main.models import Item

logger = logging.getLogger('django')


def common(request):
    if request.method == 'GET':
        data = {}
        if request.GET:
            item = _get_item(**request.GET)
        else:
            item = _get_item()

        if 'HTTP_ACCEPT' in request.META \
                and request.META['HTTP_ACCEPT'] == 'application/json':
            item = item.to_dict()
            data['item'] = item
            return JsonResponse(data)
        else:
            data = _index()
            data['item'] = item
            return render(request, 'index.html', data)
    else:
        return HttpResponseNotAllowed(['GET'])


def _index():
    cursor = None
    data = {
        'all': 0,
        'cats': []
    }
    try:
        cursor = connection.cursor()
        query = 'select mc.id, name, count(mi.id) as qty'
        query += ' from main_item mi, main_category mc'
        query += ' where mc.id = mi.category_id'
        query += ' group by mi.category_id'
        query += ' union'
        query += ' select 0, "all", count(id) as qty'
        query += ' from main_item'
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for row in result:
                if row[1] == 'all':
                    data['all'] = row[2]
                else:
                    data['cats'].append({
                        'id': row[0],
                        'name': row[1],
                        'qty': row[2]
                    })
    except Exception as ex:
        logger.error(ex)
        data['error'] = ex.__str__()
    finally:
        if cursor:
            cursor.close()
        return data


def _get_item(category_id=None, action=None, current_id=None):
    objects = Item.objects
    if category_id:
        objects = objects.filter(category_id=category_id[0])
    if action and action[0] in ['prev', 'next'] and current_id:
        if action[0] == 'prev':
            objects = objects.filter(id__lt=current_id[0]).order_by('-id')
        elif action[0] == 'next':
            objects = objects.filter(id__gt=current_id[0]).order_by('id')
        item = objects[0]
    else:
        item = objects.order_by('?').first()
    return item

