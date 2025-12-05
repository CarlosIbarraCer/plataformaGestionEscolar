from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        first = self.user.first_name if self.user else ""
        last = self.user.last_name if self.user else ""
        return f"Perfil del admin {first} {last}".strip()
    
class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255,null=True, blank=True)
    curp = models.CharField(max_length=255,null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now = True, null=True, blank=True)

    def __str__(self):
        first = self.user.first_name if self.user else ""
        last = self.user.last_name if self.user else ""
        return f"Perfil del alumno {first} {last}".strip()
    
class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    cubiculo = models.CharField(max_length=255,null=True, blank=True)
    area_investigacion = models.CharField(max_length=255,null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now = True, null=True, blank=True)

    def __str__(self):
        first = self.user.first_name if self.user else ""
        last = self.user.last_name if self.user else ""
        return f"Perfil del maestro {first} {last}".strip()


TIPO_EVENTO_CHOICES = (
    ("Conferencia", "Conferencia"),
    ("Taller", "Taller"),
    ("Seminario", "Seminario"),
    ("Concurso", "Concurso"),
)

PROGRAMA_CHOICES = (
    ("Ingenieria en Ciencias de la Computacion", "Ingenieria en Ciencias de la Computacion"),
    ("Licenciatura en Ciencias de la Computacion", "Licenciatura en Ciencias de la Computacion"),
    ("Ingenieria en Tecnologias de la Informacion", "Ingenieria en Tecnologias de la Informacion"),
)


class EventoAcademico(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=255)
    publico_objetivo = models.TextField(help_text="Lista JSON de públicos objetivo")
    programa_educativo = models.CharField(max_length=100, choices=PROGRAMA_CHOICES, null=True, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.PROTECT, related_name="eventos_responsable")
    descripcion = models.TextField()
    cupo_maximo = models.PositiveSmallIntegerField()
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Evento: {self.nombre}".strip()
