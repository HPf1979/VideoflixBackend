from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email']
        extra_kwargs = {'email': {'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        username = email  # Benutzername automatisch mit E-Mail setzen

        user = User.objects.create_user(
            username=username, email=email, password=password, **validated_data)
        return user
        
