from django.urls import path

from users.apps import UsersConfig
from users.views import UserListAPIview, UserRetrieveAPIview, UserDeleteAPIview, UserUpdateAPIview

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIview.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIview.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIview.as_view(), name='user_delete'),
    path('delete/<int:pk>/', UserDeleteAPIview.as_view(), name='user_delete')
]
