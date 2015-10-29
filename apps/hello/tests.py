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


class TestShowPage(TestCase):

    def setUp(self):
        self.person = Person.objects.first()

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


class TestPage(TestCase):
    fixtures = ['test.json', ]  # loading test fixtures

    def setUp(self):
        self.person = Person.objects.first()

    def test_check_page(self):
        """
        test check show info on main page with test fixtures
        """
        response = self.client.get(reverse('home'))
        self.assertContains(response, "42 Coffee Cups Test Assignment",
                            status_code=200)
        self.assertContains(response, "Test", status_code=200)
        self.assertContains(response, "TestTest", status_code=200)
        self.assertContains(response,
                            "born in 1900, study: school 1955-1995 years",
                            status_code=200)
        self.assertContains(response, "test@gmail.com", status_code=200)
        self.assertContains(response, "test@jabber.ru", status_code=200)
        self.assertContains(response, "test_skype", status_code=200)
        self.assertContains(response, "test test", status_code=200)


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
        self.client.get(reverse('home'))
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        response = self.client.get(reverse('home'))
        self.assertTrue("Olga" in response.content)
        self.assertTrue(Journal.objects.filter(id_item=self.person.pk))
        self.assertTrue((Journal.objects.filter(
            id_item=self.person.pk)[0]).action == 'create')
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 200)
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
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Journal.objects.filter(id_item=self.person.pk,
                                               action='create'))


class TestCustomerRequest(TestCase):

    def setUp(self):
        self.req = Requests.objects.create(
            row='dlfkgndlfkgndflkgndflkgndlfgndlfgndflgkndflg fdg dflgd',
            priority=1,
        )

    def test_if_priority_exist(self):
        """
        testing priority for saved requests - task from customer requests
        """
        self.assertEqual(self.req.priority, 1)

    def test_show_priority(self):
        """
        check if show request with priority
        """
        response = self.client.get(reverse('req'))
        self.assertEqual(self.client.get(reverse('req')).status_code, 200)
        self.assertContains(response, str(self.req.id)+'. request from ')
