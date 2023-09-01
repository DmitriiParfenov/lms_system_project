from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIview, UserListAPIview, UserRetrieveAPIview, UserDeleteAPIview, UserUpdateAPIview

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIview.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIview.as_view(), name='user_detail'),
    path('create_lesson/', UserCreateAPIview.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateAPIview.as_view(), name='user_delete'),
    path('delete/<int:pk>/', UserDeleteAPIview.as_view(), name='user_delete')
]
