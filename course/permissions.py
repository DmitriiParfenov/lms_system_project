from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrModerator(BasePermission):
    """
    Разрешает доступ по следующему принципу: а) если HTTP-методы безопасные, то доступ открывается только
    аутентифицированным пользователям; б) для PATCH- и PUT-методов — доступ только для тех пользователей, которые
    являются владельцами записи и для пользователей с расширенными правами; в) для POST-метода — доступ для
    аутентифицированных пользователей и для тех, кто не входит в группу "Moderator"; г) для DELETE-метода — доступ
    только для владельца записи или суперпользователя.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            if request.user.is_authenticated:
                return True
            return False
        elif request.method in ('PATCH', 'PUT'):
            if request.user.has_perm('course.change_course'):
                return True
            return request.user == view.get_object().user_course
        elif request.method == 'POST':
            return request.user.is_authenticated and not request.user.groups.filter(name="Moderator").exists()
        elif request.method == 'DELETE':
            return request.user == view.get_object().user_course or request.user.is_superuser
        return False

