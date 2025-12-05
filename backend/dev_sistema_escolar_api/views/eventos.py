from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from dev_sistema_escolar_api.models import EventoAcademico, Administradores, Maestros
from dev_sistema_escolar_api.serializers import EventoAcademicoSerializer, AdminSerializer, MaestroSerializer
import json


PUBLICOS_MAESTRO = ["Profesores"]
PUBLICOS_ALUMNO = ["Estudiantes"]


class EventosListCreateView(generics.ListCreateAPIView):
    serializer_class = EventoAcademicoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None  # respuestas como lista directa

    def get_queryset(self):
        user = self.request.user
        role = None
        if user and user.is_authenticated:
            groups = user.groups.all()
            role = groups[0].name if groups else None

        qs = EventoAcademico.objects.all().order_by("-fecha", "hora_inicio")
        if role == "maestro":
            filtro = Q()
            for publico in PUBLICOS_MAESTRO:
                filtro |= Q(publico_objetivo__icontains=publico)
            qs = qs.filter(filtro)
        elif role == "alumno":
            filtro = Q()
            for publico in PUBLICOS_ALUMNO:
                filtro |= Q(publico_objetivo__icontains=publico)
            qs = qs.filter(filtro)
        return qs

    def post(self, request, *args, **kwargs):
        # Solo administrador puede crear
        role = None
        if request.user and request.user.is_authenticated:
            groups = request.user.groups.all()
            role = groups[0].name if groups else None
        if role != "administrador":
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)


class EventosDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventoAcademicoSerializer
    queryset = EventoAcademico.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Reutiliza filtrado de visibilidad
        base_view = EventosListCreateView()
        base_view.request = self.request
        return base_view.get_queryset()

    def put(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def _is_admin(self):
        user = self.request.user
        groups = user.groups.all() if user and user.is_authenticated else []
        role = groups[0].name if groups else None
        return role == "administrador"


class EventoOptionsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=True)
        admins = Administradores.objects.filter(user__is_active=True)
        responsables = []
        for m in MaestroSerializer(maestros, many=True).data:
            responsables.append({
                "id": m["user"]["id"],
                "nombre": f"{m['user']['first_name']} {m['user']['last_name']}",
                "rol": "maestro"
            })
        for a in AdminSerializer(admins, many=True).data:
            responsables.append({
                "id": a["user"]["id"],
                "nombre": f"{a['user']['first_name']} {a['user']['last_name']}",
                "rol": "administrador"
            })

        tipos = [choice[0] for choice in EventoAcademico._meta.get_field("tipo").choices]
        programas = [choice[0] for choice in EventoAcademico._meta.get_field("programa_educativo").choices]
        publicos = ["Estudiantes", "Profesores", "Publico general"]

        return Response({
            "tipos": tipos,
            "publicos": publicos,
            "programas": programas,
            "responsables": responsables
        })
