from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
import random
import string
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import viewsets
from .models import Video
from .serializers import VideoSerializer


class SignupView(APIView):
    def generate_unique_confirmation_code(self):
        # ich erzeuge einen zufälligen Bestätigungscode oder Token
        code_length = 16  # Legen Sie die Länge des Codes fest
        characters = string.ascii_letters + string.digits
        confirmation_code = ''.join(random.choice(characters)
                                    for i in range(code_length))
        return confirmation_code

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # ich setze den Benutzernamen gleich der E-Mail-Adresse
            user.username = user.email
            user.save()

            self.send_confirmation_email(user)

            # ich gebe eine Erfolgsantwort zurück
            return Response({'success': True, 'user_id': user.id}, status=status.HTTP_201_CREATED)

        # Für den Fall, dass die Validierung fehlschlägt
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_confirmation_email(self, user):
        # ich generiere einen eindeutigen Bestätigungscode oder Token
        confirmation_code = self.generate_unique_confirmation_code()

        # ich speichere den Bestätigungscode oder Token im Benutzerobjekt
        user.confirmation_code = confirmation_code
        user.save()

        confirmation_link = f'http://herlina-pfeiffer.developerakademie.net/confirm?code={confirmation_code}'

       # ich sende die Bestätigungsemail mit einem blauen Link
        email_subject = 'Bestätigen Sie Ihre E-Mail-Adresse'
        email_message = f'Klicken Sie auf den folgenden Link, um Ihre E-Mail für unsere App zu bestätigen: <a href="{confirmation_link}" style="color: blue;">{confirmation_link}</a>'

        send_mail(
            email_subject,
            email_message,
            'pfeiffer.herlina@gmail.com',  # Absender-E-Mail
            [user.email],  # Empfänger-E-Mail (Benutzeremail)
            fail_silently=False,
            html_message=email_message,  # Dieser Parameter fügt HTML zur E-Mail hinzu
        )


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Wenn die Authentifizierung erfolgreich ist, wird Token generiert oder geholt
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Login fehlgeschlagen'}, status=status.HTTP_401_UNAUTHORIZED)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # basename = 'videos'

# class ProfileView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get(self, request, format=None):
    # content = {
    # 'user': str(request.user),  # `django.contrib.auth.User` instance.
    # 'auth': str(request.auth),  # None
    # }
    # return Response(content)

# class IndexView(APIView):
    # def get(self, request, format=None):
    # content = {
    #  'wsmg': 'Welcome to Full Stack Development'
    # }
    # return Response(content)
