from django.http import HttpRequest
from django.template.defaulttags import csrf_token
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
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





class ListAndItemModelsTest(TestCase):

     def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/some_list1/') #1

        self.assertContains(response, 'itemey 1') #2
        self.assertContains(response, 'itemey 2') #3


    def test_uses_list_template(self):
        response = self.client.get('/lists/some_list1/')
        self.assertTemplateUsed(response,'list.html')

class NewListTest(TestCase):


    def test_redirect_post_request(self):

        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/lists/some_list1/')
        self.assertEqual(response['location'], '/lists/some_list1/')

    def test_saving_a_post_request(self):

        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

