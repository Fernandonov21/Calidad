from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateUserView, CreateDireccionView, DeleteUserView, UpdateUserView, CustomTokenObtainPairView, ListUsersView, CreateTipoDireccionView, RetrieveUserView, ListDireccionesByUserView, UpdateDireccionView, RetrieveTipoDireccionView, ListTipoDireccionView, DeleteDireccionView, NonStaffTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('create-direccion/', CreateDireccionView.as_view(), name='create_direccion'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('list-users/', ListUsersView.as_view(), name='list_users'),
    path('create-tipo-direccion/', CreateTipoDireccionView.as_view(), name='create_tipo_direccion'),
    path('retrieve-user/<int:pk>/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('list-direcciones/<int:user_id>/', ListDireccionesByUserView.as_view(), name='list_direcciones_by_user'),
    path('update-direccion/<int:pk>/', UpdateDireccionView.as_view(), name='update_direccion'),
    path('retrieve-tipo-direccion/<int:pk>/', RetrieveTipoDireccionView.as_view(), name='retrieve_tipo_direccion'),
    path('list-tipo-direccion/', ListTipoDireccionView.as_view(), name='list_tipo_direccion'),
    path('delete-direccion/<int:pk>/', DeleteDireccionView.as_view(), name='delete_direccion'),
    path('nonstaff-login/', NonStaffTokenObtainPairView.as_view(), name='nonstaff_token_obtain_pair'),
]
