from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from .models import Direccion
from .models import TipoDireccion

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añade campos personalizados al token
        token['Nombres'] = user.Nombres
        token['Apellidos'] = user.Apellidos
        token['user_id'] = user.id  # Añadir el ID del usuario al token
        return token

    def validate(self, attrs):
        # Sobreescribir para usar CorreoElectronico en lugar de username
        self.user = CustomUser.objects.filter(CorreoElectronico=attrs['CorreoElectronico']).first()
        if not self.user or not self.user.check_password(attrs['password']):
            raise AuthenticationFailed('Credenciales inválidas')
        return super().validate(attrs)

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Hacer que el campo password no sea obligatorio

    class Meta:
        model = CustomUser
        fields = ('Nombres', 'Apellidos', 'Cedula', 'CorreoElectronico', 'password', 'TelefonoContacto')

    def validate_CorreoElectronico(self, value):
        if self.instance:
            if CustomUser.objects.filter(CorreoElectronico=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError('Este correo electrónico ya está en uso.')
        else:
            if CustomUser.objects.filter(CorreoElectronico=value).exists():
                raise serializers.ValidationError('Este correo electrónico ya está en uso.')
        return value

    def validate_Cedula(self, value):
        if self.instance:
            if CustomUser.objects.filter(Cedula=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError('Esta cédula ya está en uso.')
        else:
            if CustomUser.objects.filter(Cedula=value).exists():
                raise serializers.ValidationError('Esta cédula ya está en uso.')
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            CorreoElectronico=validated_data['CorreoElectronico'],
            password=validated_data['password'],
            Nombres=validated_data['Nombres'],
            Apellidos=validated_data['Apellidos'],
            Cedula=validated_data['Cedula'],
            TelefonoContacto=validated_data.get('TelefonoContacto', '')
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class CreateDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('id', 'Calle', 'Numero', 'Ciudad', 'Estado', 'CodigoPostal', 'Pais', 'usuario', 'tipo_direccion')

    def create(self, validated_data):
        direccion = Direccion.objects.create(
            Calle=validated_data['Calle'],
            Numero=validated_data.get('Numero', ''),
            Ciudad=validated_data['Ciudad'],
            Estado=validated_data['Estado'],
            CodigoPostal=validated_data.get('CodigoPostal', ''),
            Pais=validated_data['Pais'],
            usuario=validated_data['usuario'],
            tipo_direccion=validated_data['tipo_direccion']
        )
        return direccion

class TipoDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDireccion
        fields = ('id', 'nombre')

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'Nombres', 'Apellidos', 'Cedula', 'CorreoElectronico', 'TelefonoContacto', 'FechaCreacion')
