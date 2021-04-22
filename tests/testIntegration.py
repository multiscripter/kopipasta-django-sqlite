import re

from django.test import Client
from django.test import TestCase
from main.models.Category import Category
from main.models.Item import Item


# Запуск тестов класса через unittests:
# python manage.py test tests.testIntegration.TestIntegration

# Запуск всех тестов с покрытием через pytest:
# pytest ./tests/* --cov

# Запуск всех тестов с покрытием через unittests:
# coverage erase
# coverage run manage.py test
# coverage html

class TestIntegration(TestCase):
    """Интеграционные тесты."""

    def setUp(self):
        """Действия перед тестом."""

        self.client = Client()

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

    def test_without_request_params_html(self):
        """Вызов без request-параметров."""

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        content = response.content.decode('utf-8')
        for cat in self.categories:
            expected = len(list(filter(
                lambda item: item['category_id'] == cat.id, self.items
            )))
            exp = re.compile(f'(?<={cat.name} \()\d+')
            actual = int(exp.search(content).group(0))
            self.assertEqual(expected, actual)
