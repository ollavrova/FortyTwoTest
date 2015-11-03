# -*- coding: utf-8 -*-
import os
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context, Template
from fortytwo_test_task.settings import STATICFILES_DIRS
from apps.hello.models import Person, Requests, Journal
from django.core.urlresolvers import reverse
from django.test import TestCase
from StringIO import StringIO
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver


class TestShowPage(TestCase):

    def setUp(self):
        self.person = Person.objects.first()
        self.person1 = Person.objects.create(
            first_name="Olla",
            last_name="LLL",
            birthday="1990-01-01",
            bio="biography",
            email="google@google.com",
            jabber="xxx@jabber.org",
            skype="qwerty",
            other="qwerty qwerty qwerty",
        )

    def test_show_page(self):
        """
        test check show info on main page
        """
        response = self.client.get(reverse('home'))
        self.assertContains(response, "42 Coffee Cups Test Assignment",
                            status_code=200)
        self.assertContains(response, "Olga", status_code=200)
        self.assertContains(response, "Lavrova", status_code=200)
        self.assertContains(response, "born in 1978", status_code=200)
        self.assertContains(response, "krocozabr@gmail.com", status_code=200)
        self.assertContains(response, "ollavr@jabber.ru", status_code=200)
        self.assertContains(response, "ollavrova", status_code=200)
        self.assertContains(response, "nothing", status_code=200)

    def test_render_context(self):
        """
        test render context
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['person'], self.person)

    def test_render_cyrilic(self):
        """
        test render cyrilic text
        """
        self.person.first_name = 'Ольга'
        self.person.last_name = 'Лаврова'
        self.person.bio = 'Школа, садик, институт.'
        self.person.other = 'прочая информация'
        self.person.save()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Ольга", status_code=200)
        self.assertContains(response, "Лаврова", status_code=200)
        self.assertContains(response, "Школа, садик, институт.",
                            status_code=200)
        self.assertContains(response, "прочая информация", status_code=200)
        self.assertEqual(self.person.first_name, "Ольга")
        self.assertEqual(self.person.last_name, "Лаврова")
        self.assertEqual(self.person.bio, "Школа, садик, институт.")
        self.assertEqual(self.person.other, "прочая информация")

    def test_2_row(self):
        """
        test case if db has 2 records
        """
        self.assertEqual(Person.objects.count(), 2)
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, self.person1.first_name,

                               status_code=200)
        self.assertNotContains(response, self.person1.last_name)
        self.assertNotContains(response, self.person1.bio)
        self.assertNotContains(response, self.person1.email)
        self.assertNotContains(response, self.person1.jabber)
        self.assertNotContains(response, self.person1.skype)
        self.assertNotContains(response, self.person1.other)


class TestEmptyBase(TestCase):
    def setUp(self):
        self.person = Person.objects.first()

    def test_empty_page(self):
        """
        testing what if database is empty
        """
        Person.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.person.first_name,
                               status_code=200)
        self.assertContains(response, 'Sorry, you have an empty database now',
                            status_code=200)


class TestMiddleware(TestCase):
    def setUp(self):
        for r in range(1, 15, 1):
            Requests.objects.create(row='Example'+str(r),
                                    request_path='/example_requests/'+str(r),
                                    request_method='GET'+str(r))

    def test_middleware_show_list(self):
        """
        testing middleware, and page that show only 10 first requests
        """
        response = self.client.get(reverse('req'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Requests list:", status_code=200)
        for r in Requests.objects.all():
            if r.id <= 10:
                self.assertContains(response, r.request_path)
            else:
                self.assertNotContains(response, r.request_path)
        response = self.client.get(reverse('req'), dict(request_old_count=15),
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)

    def test_middleware_writing(self):
        """
        test middleware writing in db
        """
        count1 = Requests.objects.all().count()
        response = self.client.get(reverse('req'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/requests/',
                         Requests.objects.latest('timestamp').request_path)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/',
                         Requests.objects.latest('timestamp').request_path)
        count2 = Requests.objects.all().count()
        self.assertEqual(count2, count1+2)


class TestEditForm(TestCase):
    def setUp(self):
        self.auth = {"username": "admin", "password": "admin"}

    def test_auth(self):
        """
        testing auth to edit page
        """
        self.assertEqual(self.client.get(reverse('logout')).status_code, 302)
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('req')).status_code, 200)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 302)
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 200)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 302)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 302)

    def test_editform(self):
        """
        test edit form
        """
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 200)
        upload_file = open(os.path.join(STATICFILES_DIRS[0],
                                        'img', "test.jpg"), "rb")
        data = dict(
            first_name="Olga",
            last_name="Test",
            birthday="2000-01-01",
            bio="biography",
            email="google@google.com",
            jabber="xxx@jabber.org",
            skype="qwerty",
            other="qwerty qwerty qwerty",
            photo=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        response = self.client.post(reverse('edit'), data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response1 = self.client.get(reverse('edit'))
        self.assertContains(response1, data['first_name'])
        self.assertContains(response1, data['last_name'])
        self.assertContains(response1, data['bio'])
        self.assertContains(response1, data['email'])
        self.assertContains(response1, data['skype'])
        self.assertContains(response1, data['other'])
        response2 = self.client.get(reverse('home'))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, data['first_name'])
        self.assertContains(response2, data['last_name'])
        self.assertContains(response2, data['bio'])
        self.assertContains(response2, data['email'])
        self.assertContains(response2, data['skype'])
        self.assertContains(response2, data['other'])

    def test_show_errors(self):
        """
        test for checking show errors
        """
        self.client.post(reverse('login'), self.auth)
        data = dict(
            first_name='',
            last_name='',
            skype=''
        )
        response = self.client.post(reverse('edit'), data,
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertContains(response, 'There were some errors')
        self.assertContains(response, 'Please correct the following:')
        self.assertContains(response, 'First Name: This field is required.')
        self.assertContains(response, 'Last Name: This field is required.')
        self.assertContains(response, 'Skype: This field is required.')


class TestTemplateTag(TestCase):

    def setUp(self):
        self.person = Person.objects.create(
            first_name="Olga",
            last_name="Test",
            birthday="2000-01-01",
            bio="biography",
            email="google@google.com",
            jabber="xxx@jabber.org",
            skype="qwerty",
            other="qwerty qwerty qwerty",
        )

    def test_tag(self):
        """
        testing custom template tag for objects admin link
        """
        html = Template(
            "{% load edit_link %}"
            "{% edit_link person %}"
        ).render(Context({
            'person': self.person
        }))
        self.assertEqual(html, reverse("admin:hello_person_change",
                                       args=(self.person.pk,)))


class TestCommand(TestCase):

    def test_command(self):
        """
        testing statistic command
        """
        out = StringIO()
        management.call_command('stats', stdout=out)
        self.assertTrue("Person: 1" in out.getvalue())


class TestSignalProcessor(TestCase):

    def setUp(self):
        self.auth = {"username": "admin", "password": "admin"}
        self.person = Person.objects.create(
            first_name="Olga",
            last_name="Test",
            birthday="2000-01-01",
            bio="biography",
            email="google@google.com",
            jabber="xxx@jabber.org",
            skype="qwerty",
            other="qwerty qwerty qwerty"
        )

    def test_signals(self):
        """
        testing signals after any db action
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Olga" in response.content)
        self.assertTrue((Journal.objects.filter(
            id_item=self.person.pk)[0]).action == 'create')
        self.client.post(reverse('login'), self.auth)
        data = dict(
            pk=1,
            first_name="Test",
            last_name="User",
            birthday="1994-04-11",
            bio="biography test user",
            email="google321@google.com",
            jabber="xxx321@jabber.org",
            skype="qwerty 321",
            other="qwerty drtreter rtyht h"
        )
        response = self.client.post(reverse('edit'), data=data,
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        # check editing signal
        self.assertTrue(Journal.objects.filter(id_item=1,
                                               model_name=Person.__name__,
                                               action='edit'))
        # check creating Requests entry
        response = self.client.get(reverse('req'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Journal.objects.filter(model_name=Requests.__name__,
                                               action='create'))

class TestCustomerRequest1(TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.req1 = Requests.objects.create(
            row='dlfkgndlfkgndflkgndflkgndlfgndlfgndflgkndflg fdg dflgd',
            priority=1,
        )
        self.req2 = Requests.objects.create(
            row='dlfkgndlfkgndflkgndfgkljlklllllllndflgkndflg fdg dflgd',
            priority=0,
        )

    def test_priority(self):
        """
        check if show request with priority
        """
        # set max priority to record
        max_priority = Requests.objects.order_by('-priority')[0].priority
        self.req1.priority = max_priority+1
        self.req1.save()
        response = self.client.get(reverse('req'))

        # check if record is first in list in context
        self.assertEqual(response.context['object_list'][0], self.req)
        self.assertEqual(self.client.get(reverse('req')).status_code, 200)
        # check if equal
        self.assertSequenceEqual(Requests.objects.order_by(
            '-priority', 'timestamp')[:10],
                                 response.context['object_list']
                                 )
        self.assertContains(response, str(self.req.id)+'. request from ')
        html1 = '<p class="item-1">'+self.req1.id+'. request from'
        html2 = '<p class="item-2">'+self.req2.id+'. request from'
        self.assertContains(response, html1)
        self.assertContains(response, html2)


class TestCustomerRequest(LiveServerTestCase):
    """
    set of selenium tests
    """

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.req1 = Requests.objects.create(
            row='dlfkgndlfkgndflkgndflkgndlfgndlfgndflgkndflg fdg dflgd',
            priority=1,
        )
        self.req2 = Requests.objects.create(
            row='dlfkgndlfkgndflkgndflkgndlfgndlfgndflgkndflg fdg dflgd',
            priority=0,
        )

    def tearDown(self):
        self.browser.quit()

    def test_priority(self):
        """
        check if show request with priority
        """
        self.browser.get(self.live_server_url + '/requests')
        title = self.browser.find_element_by_class_name('main-title')
        self.assertTrue(title.is_displayed())
        self.assertTrue(title.text == 'Requests list:')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(body.text, 'request from')
        # check html in body
        html1 = '<p class="item-1">'+str(self.req1.id)+'. request from'
        html2 = '<p class="item-2">'+str(self.req2.id)+'. request from'
        self.assertContains(body.text, html1)
        self.assertContains(body.text, html2)
        # check order on the page
        css_selector1 = '#request-list:first-child'
        css_selector2 = '#request-list:nth-child(2)'
        first = self.browser.find_element_by_css_selector(css_selector1)
        second = self.browser.find_element_by_css_selector(css_selector2)
        self.assertTrue(first.is_displayed())
        self.assertContains(first, self.req1.timestamp)
        self.assertTrue(second.is_displayed())
        self.assertContains(second, self.req2.timestamp)
