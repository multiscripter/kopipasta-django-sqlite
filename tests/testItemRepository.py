from django.test import TestCase
from unittest.mock import patch

from kopipasta.models.Category import Category
from kopipasta.models.Item import Item
from kopipasta.services.ItemRepository import ItemRepository


# Запуск всех тестов с покрытием через unittests:
# coverage erase
# coverage run manage.py test
# coverage html


class TestItemRepository(TestCase):
    """Unit-тесты ItemRepository."""

    def setUp(self):
        """Действия перед тестом."""

        self.categories = []
        for name in ['Трах и ненависть', 'Мыты']:
            category = Category()
            category.name = name
            category.save()
            self.categories.append(category)

        self.items = []
        for cat in self.categories:
            for a in range(1, 4):
                item = Item()
                item.title = f'имя-{a}'
                item.text = f'текст {a}'
                item.category = cat
                item.save()
                self.items.append(item.to_dict())

    @patch('django.db.connection.cursor')
    def test_get_category_data_throws_exception(self, mocked_cursor):
        """Тестирует get_category_data(self).
        Выбрасывает Exception."""

        error_message = 'Custom exception message'
        mocked_cursor.side_effect = Exception(error_message)

        expected = {
            'all': 0,
            'cats': [],
            'error': error_message
        }

        actual = ItemRepository().get_category_data()
        self.assertEqual(expected, actual)
