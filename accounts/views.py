from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import CreateUserSerializer
from rest_framework import generics
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import CreateDireccionSerializer
from .models import Direccion
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import ListUserSerializer
from .serializers import TipoDireccionSerializer
from .models import TipoDireccion

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.filter(CorreoElectronico=request.data.get('CorreoElectronico')).first()
        if user and not user.is_staff:
            return Response({'detail': 'Solo los usuarios administradores pueden acceder.'}, status=status.HTTP_403_FORBIDDEN)
        return response

class NonStaffTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.filter(CorreoElectronico=request.data.get('CorreoElectronico')).first()
        if user and user.is_staff:
            return Response({'detail': 'Los usuarios administradores no pueden acceder.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Añadir el ID del usuario a la respuesta
        if response.status_code == 200:
            response.data['user_id'] = user.id
        return response

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

class CreateDireccionView(generics.CreateAPIView):
    queryset = Direccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateDireccionSerializer

class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.direccion_set.all().delete()  # Eliminar todas las direcciones asociadas
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer

class CreateTipoDireccionView(generics.CreateAPIView):
    queryset = TipoDireccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TipoDireccionSerializer

class RetrieveUserView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer

class ListDireccionesByUserView(generics.ListAPIView):
    serializer_class = CreateDireccionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Direccion.objects.filter(usuario_id=user_id)

class UpdateDireccionView(generics.UpdateAPIView):
    queryset = Direccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateDireccionSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Direccion.DoesNotExist:
            raise Response({'detail': 'No Direccion matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

class RetrieveTipoDireccionView(generics.RetrieveAPIView):
    queryset = TipoDireccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TipoDireccionSerializer

class ListTipoDireccionView(generics.ListAPIView):
    queryset = TipoDireccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TipoDireccionSerializer

class DeleteDireccionView(generics.DestroyAPIView):
    queryset = Direccion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateDireccionSerializer
