from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIview, UserRetrieveAPIview, UserDeleteAPIview, UserUpdateAPIview

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIview.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIview.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIview.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteAPIview.as_view(), name='user_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
