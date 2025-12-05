from django.contrib.auth.models import User
from rest_framework import serializers
from dev_sistema_escolar_api.models import *
import datetime
import json
import re

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'


class EventoAcademicoSerializer(serializers.ModelSerializer):
    publico_objetivo = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    responsable_nombre = serializers.SerializerMethodField()

    class Meta:
        model = EventoAcademico
        fields = '__all__'

    def get_responsable_nombre(self, obj):
        first = obj.responsable.first_name or ""
        last = obj.responsable.last_name or ""
        return (first + " " + last).strip() or obj.responsable.username

    def validate(self, attrs):
        nombre = attrs.get("nombre", "").strip()
        lugar = attrs.get("lugar", "").strip()
        descripcion = attrs.get("descripcion", "").strip()
        fecha = attrs.get("fecha")
        hora_inicio = attrs.get("hora_inicio")
        hora_fin = attrs.get("hora_fin")
        publico_objetivo = attrs.get("publico_objetivo", [])
        programa_educativo = attrs.get("programa_educativo")
        cupo = attrs.get("cupo_maximo")

        regex_nombre = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+$")
        regex_lugar = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ,.\-]+$")
        regex_desc = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ,.;:()\-\n\r]+$")

        if not nombre or not regex_nombre.match(nombre):
            raise serializers.ValidationError("Nombre del evento inválido")
        if not lugar or not regex_lugar.match(lugar):
            raise serializers.ValidationError("Lugar inválido")
        if not descripcion or len(descripcion) > 300 or not regex_desc.match(descripcion):
            raise serializers.ValidationError("Descripción inválida")

        if not fecha or fecha < datetime.date.today():
            raise serializers.ValidationError("La fecha no puede ser anterior a hoy")
        if not hora_inicio or not hora_fin or hora_inicio >= hora_fin:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora fin")
        if cupo is None or cupo <= 0 or cupo > 999:
            raise serializers.ValidationError("Cupo máximo inválido")

        # Público objetivo como lista
        publicos = []
        publicos = publico_objetivo if isinstance(publico_objetivo, list) else []
        if not publicos or not isinstance(publicos, list):
            raise serializers.ValidationError({"publico_objetivo": "Público objetivo requerido"})

        if "Estudiantes" in publicos and not programa_educativo:
            raise serializers.ValidationError({"programa_educativo": "Programa educativo es obligatorio para estudiantes"})

        # Normalizar cadenas
        attrs["nombre"] = nombre
        attrs["lugar"] = lugar
        attrs["descripcion"] = descripcion
        attrs["publico_objetivo"] = json.dumps(publicos)
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data["publico_objetivo"] = json.loads(data.get("publico_objetivo") or "[]")
        except Exception:
            data["publico_objetivo"] = []
        return data
