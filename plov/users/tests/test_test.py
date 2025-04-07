import django.test
import django.urls


class TestTestCase(django.test.TestCase):
    def test_test(self):
        self.assertEqual(2 + 2, 4, msg='Стоп, что?!')
