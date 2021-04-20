from django.db import connection
from django.http import HttpResponse, Http404
from django.shortcuts import render
import logging

from main.models import Item

logger = logging.getLogger(__name__)


def common(request):
    if request.method == 'GET':
        if request.GET:
            print(request.GET)
            return HttpResponse('the Copy-paste index.')
        else:
            data = _index()
            return render(request, 'index.html', data)
    else:
        raise Http404


def _index():
    cursor = None
    data = {
        'all': 0,
        'cats': [],
        'item': None
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
    finally:
        if cursor:
            cursor.close()
    data['item'] = _get_item()
    return data


def _get_item(category_id=None, action=None, current_id=None):
    objects = Item.objects
    if category_id:
        objects = objects.filter(category_id=category_id)
    if action in ['prev', 'next'] and current_id:
        if action == 'prev':
            objects = objects.filter(id__lte=current_id)
        elif action == 'next':
            objects = objects.filter(id__gte=current_id)
        item = objects[0]
    else:
        item = objects.order_by('?').first()
    return item
