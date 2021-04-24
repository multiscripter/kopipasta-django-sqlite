from django.test import TestCase

from kopipasta.services.validation import validate

# Запуск тестов класса через unittests:
# python manage.py test tests.testValidation.TestValidation


class TestValidation(TestCase):
    """Тестирует валидацию."""

    def test_error_not_a_number(self):
        """Ошибка: Not a number."""

        expected = {'category_id': 'Not a number'}

        params = {'category_id': '1.5'}
        actual = validate(params)
        self.assertEqual(expected, actual)

    def test_error_less_than_one(self):
        """Ошибка: Less than one."""

        expected = {'category_id': 'Less than one'}

        params = {'category_id': '0'}
        actual = validate(params)
        self.assertEqual(expected, actual)

    def test_error_unknown_action(self):
        """Ошибка: Unknown action."""

        expected = {'action': 'Unknown action'}

        params = {'action': 'random'}
        actual = validate(params)
        self.assertEqual(expected, actual)
