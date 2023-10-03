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
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def send_email_confirmation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Versuchen, die E-Mail zu senden
            send_mail(
                'Bestätigen Sie Ihre E-Mail-Adresse',
                'Klicken Sie auf den folgenden Link, um Ihre E-Mail zu bestätigen: [Bestätigungslink]',
                'pfeiffer.herlina@gmx.net',  # Absender-E-Mail
                [email],  # Empfänger-E-Mail
                fail_silently=False,
            )
            # Wenn erfolgreich, eine Erfolgsmeldung zurückgeben
            return JsonResponse({'message': 'Bestätigungsemail wurde gesendet'})
        except Exception as e:
            # Wenn ein Fehler auftritt, eine Fehlermeldung zurückgeben
            return JsonResponse({'message': f'Fehler beim Senden der E-Mail: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Ungültige Anfrage'}, status=400)


#class ProfileView(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    #def get(self, request, format=None):
        #content = {
           # 'user': str(request.user),  # `django.contrib.auth.User` instance.
            #'auth': str(request.auth),  # None
        #}
        #return Response(content)
    
#class IndexView(APIView):
       #def get(self, request, format=None):
       # content = {
          #  'wsmg': 'Welcome to Full Stack Development'
        #}
        #return Response(content)