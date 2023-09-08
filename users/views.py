from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from users.models import User
from users.permissions import IsAuthenticatedAndOwner
from users.serializers import UserSerializer, UserUpdateSerializer, UserSerializerForPayment


# Create your views here.
class UserListAPIview(generics.ListAPIView):
    """Для получения всех объектов модели User."""

    serializer_class = UserSerializerForPayment
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedAndOwner,)


class UserRetrieveAPIview(generics.RetrieveAPIView):
    """Для детализацаии 1 объекта модели User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedAndOwner,)


class UserUpdateAPIview(generics.UpdateAPIView):
    """Для обновления объектов модели User."""

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedAndOwner,)


class UserDeleteAPIview(generics.DestroyAPIView):
    """Для удаления объектов модели User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
