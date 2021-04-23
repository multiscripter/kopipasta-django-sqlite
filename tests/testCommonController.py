import json
import re

from django.http import HttpRequest, QueryDict
from django.test import TestCase

from main.controllers.common import common, http400, http403, http404, http500
from main.models.Category import Category
from main.models.Item import Item


# Запуск тестов класса через unittests:
# python manage.py test tests.testCommonController.TestCommonController

# Запуск всех тестов с покрытием через pytest:
# pytest ./tests/* --cov

# Запуск всех тестов с покрытием через unittests:
# coverage erase
# coverage run manage.py test
# coverage html


class TestCommonController(TestCase):
    """Unit-тесты контроллера common."""

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

    def test_common_without_request_params_html(self):
        """Тестирует common.common(request).
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

    def test_common_get_random_no_category_html(self):
        """Тестирует common.common(request).
        request-параметры: action=random
        Content-Type: text/html"""

        request = HttpRequest()
        request.method = 'GET'
        request.GET = QueryDict(query_string='action=random')
        response = common(request)
        self.assertEqual(200, response.status_code)

        content = response.content.decode('utf-8')
        exp = re.compile(f'(?<=pasta-head")[^<]+')
        actual = exp.search(content).group(0)
        exp = re.compile(f'(?<=>).*')
        actual = exp.search(actual).group(0)
        self.assertTrue(actual)

    def test_common_http_method_post_error_405(self):
        """Тестирует common.common(request).
        HTTP-метод: POST.
        Ошибка: 405 Method Not Allowed."""

        request = HttpRequest()
        request.method = 'POST'
        response = common(request)
        self.assertEqual(405, response.status_code)
        self.assertEqual('GET', response.headers['Allow'])

    def test_common_get_random_no_category_json(self):
        """Тестирует common.common(request).
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
        """Тестирует common.common(request).
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
        """Тестирует common.common(request).
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
        """Тестирует common.common(request).
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

    def test_common_get_first_no_category_json(self):
        """Тестирует common.common(request).
        request-параметры: action=first
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = 'action=first'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(self.items[0], data['item'])

    def test_common_get_last_no_category_json(self):
        """Тестирует common.common(request).
        request-параметры: action=last
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = 'action=last'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(self.items[len(self.items) - 1], data['item'])

    def test_common_get_prev_with_category_json(self):
        """Тестирует common.common(request).
        request-параметры: category_id=2, action=prev, current_id=2
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = 'current_id=2&action=prev&category_id=2'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(self.items[3], data['item'])

    def test_common_get_next_with_category_json(self):
        """Тестирует common.common(request).
        request-параметры: category_id=1, action=next, current_id=5
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'
        query_str = 'current_id=5&action=next&category_id=1'
        request.GET = QueryDict(query_string=query_str)
        response = common(request)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertEqual(self.items[2], data['item'])

    def test_http400_json(self):
        """Тестирует http400(request, exception).
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'

        response = http400(request, Exception())
        self.assertEqual(400, response.status_code)

        expected = {'code': 400, 'text': 'Плохой запрос'}
        actual = json.loads(response.content)
        self.assertEqual(expected, actual)

    def test_http403_json(self):
        """Тестирует http403(request, exception).
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'

        response = http403(request, Exception())
        self.assertEqual(403, response.status_code)

        expected = {'code': 403, 'text': 'Доступ запрещён'}
        actual = json.loads(response.content)
        self.assertEqual(expected, actual)

    def test_http404_json(self):
        """Тестирует http404(request, exception).
        Content-Type: application/json"""

        request = HttpRequest()
        request.method = 'GET'
        request.META['HTTP_ACCEPT'] = 'application/json'

        response = http404(request, Exception())
        self.assertEqual(404, response.status_code)

        expected = {'code': 404, 'text': 'Страница не&nbsp;найдена'}
        actual = json.loads(response.content)
        self.assertEqual(expected, actual)

    def test_http500_html(self):
        """Тестирует http500(request, exception)."""

        request = HttpRequest()
        request.method = 'GET'

        response = http500(request)
        self.assertEqual(500, response.status_code)

        content = response.content.decode('utf-8')
        actual = re.findall('Ошибка сервера', content, re.MULTILINE)
        self.assertEqual(2, len(actual))
