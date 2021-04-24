from django.db import connection
import logging
from main.models.Item import Item


class ItemRepository:
    """Репозиторий элементов."""

    def __init__(self):
        self.logger = logging.getLogger('django')

    def get_category_data(self):
        """Получает статистические данные категорий."""

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
            self.logger.error(ex)
            data['error'] = ex.__str__()
        finally:
            if cursor:
                cursor.close()
            return data

    def get_item(self, category_id=None, action=None, current_id=None):
        """
        Получает элемент.
        :param category_id: int идентификатор категории.
        :param action: str действие.
        :param current_id: int идентификатор текущего элемента.
        :return: элемент.
        """

        data = {
            'item': None,
            'pos': None
        }
        objects = Item.objects

        if category_id and int(category_id[0]) > 0:
            objects = objects.filter(category_id=category_id[0])

        if action and action[0] in ['first', 'last']:
            if action[0] == 'first':
                objects = objects.order_by('id')
                data['pos'] = 'first'
            elif action[0] == 'last':
                objects = objects.order_by('-id')
                data['pos'] = 'last'

        elif action and action[0] in ['prev', 'next'] and current_id:
            if action[0] == 'prev':
                objects = objects.filter(id__lt=current_id[0]).order_by('-id')
                if not objects.count():
                    data = self.get_item(category_id, ['first'])
                elif objects.count() == 1:
                    data['pos'] = 'first'

            elif action[0] == 'next':
                objects = objects.filter(id__gt=current_id[0]).order_by('id')
                if not objects.count():
                    data = self.get_item(category_id, ['last'])
                elif objects.count() == 1:
                    data['pos'] = 'last'

        else:
            objects = objects.order_by('?')

        if len(objects):
            data['item'] = objects[0]
        return data
