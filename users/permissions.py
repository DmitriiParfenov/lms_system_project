from rest_framework.permissions import BasePermission


class IsAuthenticatedAndOwner(BasePermission):
    """
    Доступ разрешен только аутентифицированным пользователям. Детали записей могут смотреть только владельцы записи.
    Однако усеченная информация (без пароля, фамилии и платежей) о пользователя доступна аутентифицированным
    пользователям.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.email == obj.email:
            return True
        return False
