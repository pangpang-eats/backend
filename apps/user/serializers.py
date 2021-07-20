from typing import Dict
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.user.models import User, UserRole


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     validators=(validate_password, ))
    role = serializers.ChoiceField(read_only=True, choices=UserRole.choices)
    is_verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: Dict):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'name', 'role', 'is_verified',
                  'date_joined')