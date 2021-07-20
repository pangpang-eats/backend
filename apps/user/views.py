from django.http.request import HttpRequest
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.user.models import User
from apps.user.serializers import UserRegisterSerializer, UserSerializer


class UserView(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'register':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
        return UserSerializer

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserRegisterSerializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)