from typing import Dict
from django.http.request import HttpRequest
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.user.models import User
from apps.user.serializers import UserPasswordSetSerializer, UserRegisterSerializer, UserSerializer


class UserView(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'register':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
        if self.action == 'set_password':
            return UserPasswordSetSerializer
        return UserSerializer

    def update_profile(self, user, data) -> Dict:
        serializer: UserSerializer = UserSerializer(user,
                                                    data=data,
                                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @action(methods=['get', 'patch'], detail=False)
    def profile(self, request: HttpRequest):
        user: User = request.user
        if request.method == 'GET':  # return user's profile
            serializer: UserSerializer = self.get_serializer(user)
            return Response(serializer.data)
        # if request.method == 'PATCH'
        updated_data = self.update_profile(user, request.data)
        return Response(updated_data)

    @action(methods=['post'], detail=False)
    def set_password(self, request: HttpRequest):
        user: User = request.user
        serializer: UserPasswordSetSerializer = self.get_serializer(
            user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserRegisterSerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)