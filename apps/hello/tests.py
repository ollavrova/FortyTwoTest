# -*- coding: utf-8 -*-
from apps.hello.models import Person
from django.core.urlresolvers import reverse
from django.test import TestCase


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
