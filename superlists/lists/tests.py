from django.http import HttpRequest
from django.template.defaulttags import csrf_token
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
import re
# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
    # this test will not pass because render_to_string only takes the html and does not insert template vars
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        response_str = response.content.decode('utf-8')
        token_value = re.search("value='(.*)'",response_str).group(1)

        expected_html = render_to_string('home.html',
                                         {'new_item_text': 'A new list item',
                                            'csrf_token': token_value,
                                          }
                                         )
        self.assertEqual(response.content.decode('utf-8'), expected_html)

    def test_home_page_return_real_html_response(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode('utf-8'))