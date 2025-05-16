# -*- coding: utf-8 -*-
import pytest
from django.urls import reverse
from django.test import Client
from dbmodels.models import Users

INVALID_EMAIL = 'wrong@example.com'
INVALID_PASS = 'wrongpass'  

@pytest.mark.django_db
class TestLoginViews:

    def setup_method(self):
        self.client = Client()

    def test_root_redirect(self):
        response = self.client.get(reverse('root_redirect'))
        assert response.status_code == 302  # Redirecciona

    def test_login_form_view(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        assert b"login" in response.content.lower()

    def test_login_submit_view_invalid(self):
        # Intentar login con datos vacíos o inválidos
        response = self.client.post(
            reverse('login_submit'),
            {'email': INVALID_EMAIL, 'password': INVALID_PASS}
        )
        assert response.status_code == 200
        assert 'Credenciales inválidas' in response.content.decode('utf-8')

    def test_login_submit_view_valid(self):
        user = Users.objects.create(
            email='test@example.com',
            name='Test User',
            id_card='123456789',
            phone='1234567890',
            role_id=1,
            status=True,
        )
        user.set_password('testpassword')
        user.save()

        response = self.client.post(
            reverse('login_submit'),
            {'email': 'test@example.com', 'password': 'testpassword'}
        )
        assert response.status_code == 302  # Redirecciona al /products/
        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies

    def test_logout_view(self):
        response = self.client.post(reverse('logout'))
        assert response.status_code == 302
        assert 'access_token' not in response.cookies
        assert 'refresh_token' not in response.cookies

    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        assert response.status_code == 200
