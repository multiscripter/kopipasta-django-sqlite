import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from main.models.Category import Category
from main.models.Item import Item


# Запуск тестов класса:
# python manage.py test tests.testFunctional.TestFunctional


class TestFunctional(StaticLiveServerTestCase):
    """Функциональные тесты."""

    @classmethod
    def setUpClass(cls):
        """Действия перед всеми тестами."""
        exit(1)
        super(TestFunctional, cls).setUpClass()

        path = os.path.dirname(__file__)
        # https://github.com/mozilla/geckodriver/releases
        cls.browser = webdriver.Firefox(executable_path=path + '/../geckodriver')

        cls.categories = []
        for name in ['Трах и ненависть', 'Мыты']:
            category = Category()
            category.name = name
            category.save()
            cls.categories.append(category)

        cls.items = []
        for cat in cls.categories:
            for a in range(1, 4):
                item = Item()
                item.title = f'имя-{a}'
                item.text = f'текст {a}'
                item.category = cat
                item.save()
                cls.items.append(item.to_dict())

    def test_home_page(self):
        """Тестирует главную страницу."""

        self.browser.get(self.live_server_url)
        self.assertEqual('Копипаста', self.browser.title)

        # Сравнить h1 страницы.
        actual = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Копипастаv1', actual)

    @classmethod
    def tearDownClass(cls):
        """Действия после всех тестов."""

        cls.browser.stop_client()
        super(TestFunctional, cls).tearDownClass()
