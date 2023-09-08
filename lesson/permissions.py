from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrIsAuthenticatedOrModerator(BasePermission):
    """
    Разрешает доступ по следующему принципу: а) если HTTP-методы безопасные, то доступ открывается только
    аутентифицированным пользователям; б) для PATCH- и PUT-методов — доступ только для тех пользователей, которые
    являются владельцами записи и для пользователей с расширенными правами; в) для POST-метода — доступ для
    аутентифицированных пользователей и для тех, кто не входит в группу "Moderator"; г) для DELETE-метода — доступ
    только для владельца записи или суперпользователя.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Moderator').exists():
                if request.method in ('POST', 'DELETE'):
                    return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user.has_perm('lesson.view_lesson'):
                return True
            return request.user == obj.user_lesson
        elif request.method in ('PATCH', 'PUT'):
            if request.user.has_perm('lesson.change_lesson'):
                return True
            return request.user == obj.user_lesson
        elif request.method == 'POST':
            return request.user.is_authenticated and not request.user.groups.filter(name="Moderator").exists()
        elif request.method == 'DELETE':
            return request.user == obj.user_lesson or request.user.is_superuser
        return False
