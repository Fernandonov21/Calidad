from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, CorreoElectronico, password=None, **extra_fields):
        if not CorreoElectronico:
            raise ValueError('El correo electrónico es obligatorio')
        correo_normalizado = self.normalize_email(CorreoElectronico)
        extra_fields.setdefault('is_active', True)
        user = self.model(CorreoElectronico=correo_normalizado, **extra_fields)
        if password:  # Django usa 'password' como argumento
            user.set_password(password)  # Cifra la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, CorreoElectronico, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(CorreoElectronico, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, db_column='ID_Usuario')
    Nombres = models.CharField(max_length=100, db_column='Nombres', default='Nombre')
    Apellidos = models.CharField(max_length=100, db_column='Apellidos', default='Apellido')
    Cedula = models.CharField(max_length=20, unique=True, db_column='Cedula', default='00000000')
    CorreoElectronico = models.EmailField(unique=True, db_column='CorreoElectronico')
    password = models.CharField(max_length=255, db_column='Contraseña')
    TelefonoContacto = models.CharField(max_length=15, blank=True, null=True, db_column='TelefonoContacto')
    FechaCreacion = models.DateTimeField(auto_now_add=True, db_column='FechaCreacion')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'CorreoElectronico'
    REQUIRED_FIELDS = ['Nombres', 'Apellidos', 'Cedula']

    def __str__(self):
        return self.CorreoElectronico

    class Meta:
        db_table = 'usuarios'

class CorreoElectronico(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='ID_Usuario')
    CorreoElectronico = models.EmailField(db_column='CorreoElectronico')

    class Meta:
        db_table = 'correoselectronicos'

class TipoDireccion(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID_TipoDireccion')
    nombre = models.CharField(max_length=50, db_column='Nombre')

    class Meta:
        db_table = 'tipos_direccion'

class Direccion(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID_Direccion')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='ID_Usuario')
    Calle = models.CharField(max_length=100, db_column='Calle')
    Numero = models.CharField(max_length=10, blank=True, null=True, db_column='Numero')
    Ciudad = models.CharField(max_length=50, db_column='Ciudad')
    Estado = models.CharField(max_length=50, db_column='Estado')
    CodigoPostal = models.CharField(max_length=10, blank=True, null=True, db_column='CodigoPostal')
    Pais = models.CharField(max_length=50, db_column='Pais')
    FechaCreacion = models.DateTimeField(auto_now_add=True, db_column='FechaCreacion')
    tipo_direccion = models.ForeignKey(TipoDireccion, on_delete=models.CASCADE, db_column='ID_TipoDireccion')

    class Meta:
        db_table = 'direcciones'
