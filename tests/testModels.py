from django.test import TestCase

from kopipasta.models.Category import Category
from kopipasta.models.Item import Item


class TestModels(TestCase):
    """Unit-тесты моделей."""

    def setUp(self):
        """Действия перед тестом."""

        self.category_name = 'Тестовая категория'
        self.category = Category()
        self.category.name = self.category_name
        self.category.save()

        self.item_title = 'Тестовый заголовок'
        self.item = Item()
        self.category = self.category
        self.item.title = self.item_title
        self.item.text = 'Тестовый текст'
        self.item.save()

    def test_category_str(self):
        """Тестирует перегруженный __str__(self)"""

        self.assertEqual(self.category_name, self.category.__str__())

    def test_item_str(self):
        """Тестирует перегруженный __str__(self)"""

        self.assertEqual(self.item_title, self.item.__str__())
