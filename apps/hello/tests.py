# -*- coding: utf-8 -*-
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from fortytwo_test_task.settings import STATICFILES_DIRS
from apps.hello.models import Person, Requests
from django.core.urlresolvers import reverse
from django.test import TestCase


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
        self.person = Person.objects.first()

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
        # print os.path.join(STATICFILES_DIRS[0], 'img', "test.jpg"), 'exist'
        data = dict(
            first_name="Test",
            last_name="User",
            birthday="1994-04-11",
            bio="biography test user",
            email="google321@google.com",
            jabber="xxx321@jabber.org",
            skype="qwerty 321",
            other="qwerty drtreter rtyht h",
            photo=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        upload_file.seek(0)
        data1 = dict(
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
        response = self.client.post(reverse('edit'), data1,
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.client.get(reverse('home'))
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.person.first_name, "Olga")
        self.assertEqual(self.person.last_name, "Test")
        self.assertEqual(self.person.birthday, "2000-01-01")
        self.assertEqual(self.person.bio, "biography")
        self.assertEqual(self.person.email, "google@google.com")
        self.assertEqual(self.person.jabber, "xxx@jabber.org")
        self.assertEqual(self.person.skype, "qwerty")
        self.assertEqual(self.person.other, "qwerty qwerty qwerty")
