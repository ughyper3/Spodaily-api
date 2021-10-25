from django.test import TestCase
from django.urls import resolve

from spodaily_api.views import *


class LoginTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_redirection(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('home'))
        self.failUnlessEqual(response.status_code, 200)
        self.client.logout()


class HomeTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_home_not_authenticated_user(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/home.html')
        self.assertEqual(response.status_code, 302)

    def test_home_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/home.html')
        self.client.logout()


class AddSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_add_session_not_authenticated_user(self):
        url = reverse('add_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/add_session.html')
        self.assertEqual(response.status_code, 302)

    def test_add_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('add_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/add_session.html')
        self.client.logout()


class AddActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_add_activity_not_authenticated_user(self):
        url = reverse('add_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/add_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_add_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('add_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/add_activity.html')
        self.client.logout()


class DeleteSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_delete_session_not_authenticated_user(self):
        url = reverse('delete_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/delete_session.html')
        self.assertEqual(response.status_code, 302)

    def test_delete_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_session', args=[self.session.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/delete_session.html')
        self.client.logout()


class RegisterTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_redirection(self):
        response = self.client.post(reverse('register'),
                                    data={'email': 'alice@example.com',
                                          'password1': 'testtesttest',
                                          'password2': 'testtesttest'})
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)


class AccountTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_account_not_authenticated_user(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/account.html')
        self.assertEqual(response.status_code, 302)

    def test_account_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/account.html')
        self.client.logout()


class LogoutTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_logout_not_authenticated_user(self):
        url = reverse('routine')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/logged_out.html')
        self.assertEqual(response.status_code, 302)

    def test_logout_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        self.client.logout()


class RoutineTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_routine_not_authenticated_user(self):
        url = reverse('routine')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/routine.html')
        self.assertEqual(response.status_code, 302)

    def test_routine_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('routine'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/routine.html')
        self.client.logout()


class PastSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_past_session_not_authenticated_user(self):
        url = reverse('past_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/past_session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('past_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/past_session.html')
        self.client.logout()


class ContactTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_contact_not_authenticated_user(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/contact.html')
        self.assertEqual(response.status_code, 302)

    def test_contact_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/contact.html')
        self.client.logout()


class RulesOfUseTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_rules_of_use_not_authenticated_user(self):
        url = reverse('rules_of_use')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/rules_of_use.html')
        self.assertEqual(response.status_code, 302)

    def test_rules_of_use_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('rules_of_use'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/rules_of_use.html')
        self.client.logout()