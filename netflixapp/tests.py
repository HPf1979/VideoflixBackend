from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Video
import uuid 

class SignupLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_view(self):
        # eine eindeutige E-Mail-Adresse für den Test generieren
        test_email = f'test_user_{uuid.uuid4()}@gmail.com'
        
        data = {'email': test_email, 'password': 'testpassword'}
        response = self.client.post(reverse('signup'), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('success' in response.data)

        # um zu überprüfen, ob der Benutzer in der Datenbank erstellt wurde
        user_exists = User.objects.filter(email=test_email).exists()
        self.assertTrue(user_exists)

    def test_login_view(self):
        # Annahme: Der Benutzer wurde bereits über die Sign-up-Ansicht erstellt
        
        # eine eindeutige E-Mail-Adresse für den Testbenutzer generieren
        test_email = f'test_user_{uuid.uuid4()}@gmail.com'
        test_password = 'testpassword'

        # den Benutzer über die Sign-up-Ansicht erstellen
        signup_data = {'email': test_email, 'password': test_password}
        signup_response = self.client.post(reverse('signup'), signup_data, format='json')
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)

        # die Login-Ansicht testen
        login_data = {'email': test_email, 'password': test_password}
        login_response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in login_response.data) 

    def test_video_list_view(self):
        # Video-Listeansicht testen
        Video.objects.create(title='Test Video', description='This is a test video')

        # den Routennamen für die Video-Liste verwwenden
        response = self.client.get(reverse('video-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
