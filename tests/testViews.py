import json
import re
from unittest.mock import patch

from django.http import HttpRequest, QueryDict
from django.test import TestCase

from main.models import Category, Item
from main.views import common, _index


class TestViews(TestCase):
    """Unit-тесты view."""

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

    def test_common_without_request_params(self):
        """Тестирует views.common(request).
        Вызов без request-параметров."""

        request = HttpRequest()
        request.method = 'GET'
        response = common(request)
        self.assertEqual(200, response.status_code)

        content = response.content.decode('utf-8')
        for cat in self.categories:
            expected = len(list(filter(
                lambda item: item['category_id'] == cat.id, self.items
            )))
            exp = re.compile(f'(?<={cat.name} \()\d+')
            actual = int(exp.search(content).group(0))
            self.assertEqual(expected, actual)

    def test_common_http_method_post_error_405(self):
        """Тестирует views.common(request).
        HTTP-метод: POST.
        Ошибка: 405 Method Not Allowed."""

        request = HttpRequest()
        request.method = 'POST'
        response = common(request)
        self.assertEqual(405, response.status_code)
        self.assertEqual('GET', response.headers['Allow'])

    def test_common_get_random_no_category_html(self):
        """Тестирует views.common(request).
        request-параметры: action=random
        Content-Type: text/html"""

        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict(query_string='action=random')
        response = common(request)
        self.assertEqual(200, response.status_code)

        content = response.content.decode('utf-8')
        exp = re.compile(f'(?<=pasta-head">)\w+')
        actual = exp.search(content).group(0)
        self.assertTrue(actual)

    def test_common_get_random_no_category_json(self):
        """Тестирует views.common(request).
        request-параметры: action=random,
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        request.GET = QueryDict(query_string='action=random')
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertTrue(data['item']['id'])
        self.assertTrue(data['item']['title'])
        self.assertTrue(data['item']['text'])

    def test_common_get_random_with_category_json(self):
        """Тестирует views.common(request).
        request-параметры: action=random, category_id
        Content-Type: application/json"""

        cat_id = 1
        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = f'action=random&category_id={cat_id}'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertIn(data['item'], self.items)

    def test_common_get_prev_no_category_json(self):
        """Тестирует views.common(request).
        request-параметры: action=prev, current_id
        Content-Type: application/json"""

        current_id = 5
        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = f'action=prev&current_id={current_id}'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(current_id - 1, data['item']['id'])

    def test_common_get_next_no_category_json(self):
        """Тестирует views.common(request).
        request-параметры: action=next, current_id
        Content-Type: application/json"""

        current_id = 3
        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = f'action=next&current_id={current_id}'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(current_id + 1, data['item']['id'])

    @patch('django.db.connection.cursor')
    def test_index_throws_exception(self, mocked_cursor):
        """Тестирует _index().
        Выбрасывает Exception."""
        error_message = 'Custom exception message'
        mocked_cursor.side_effect = Exception(error_message)

        expected = {
            'all': 0,
            'cats': [],
            'error': error_message
        }

        actual = _index()
        self.assertEqual(expected, actual)
