from django.http.request import HttpRequest
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.user.models import User
from apps.user.serializers import UserSerializer


class UserView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def list(self, request: HttpRequest):  # retrieve requested user's profile
        user: User = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)