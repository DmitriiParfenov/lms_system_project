from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserListAPIview(generics.ListAPIView):
    """Для получения всех объектов модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIview(generics.RetrieveAPIView):
    """Для детализацаии 1 объекта модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIview(generics.UpdateAPIView):
    """Для обновления объектов модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteAPIview(generics.DestroyAPIView):
    """Для удаления объектов модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
