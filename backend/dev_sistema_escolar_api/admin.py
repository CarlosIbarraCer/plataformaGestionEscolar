from django.contrib import admin
from django.utils.html import format_html
from dev_sistema_escolar_api.models import Administradores, Alumnos, Maestros, EventoAcademico


@admin.register(Administradores)
@admin.register(Alumnos)
@admin.register(Maestros)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

    def _user_groups(self, request):
        if not request.user.is_authenticated:
            return set()
        return set(request.user.groups.values_list("name", flat=True))

    def _maestro_can_manage_alumnos(self, request):
        groups = self._user_groups(request)
        return "maestro" in groups or "administrador" in groups

    def _admin_can_manage_maestros_or_alumnos(self, request):
        groups = self._user_groups(request)
        return "administrador" in groups

    def _has_list_permission(self, request):
        if request.user.is_superuser:
            return True
        if self.model is Alumnos and self._maestro_can_manage_alumnos(request):
            return True
        if self.model is Maestros and self._admin_can_manage_maestros_or_alumnos(request):
            return True
        if self.model is Administradores and self._admin_can_manage_maestros_or_alumnos(request):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if self._has_list_permission(request):
            return True
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if self._has_list_permission(request):
            if self.model is Alumnos and self._maestro_can_manage_alumnos(request):
                return True
            if self.model in (Maestros, Administradores) and self._admin_can_manage_maestros_or_alumnos(request):
                return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self._has_list_permission(request):
            if self.model is Alumnos and self._maestro_can_manage_alumnos(request):
                return True
            if self.model in (Maestros, Administradores) and self._admin_can_manage_maestros_or_alumnos(request):
                return True
        return super().has_delete_permission(request, obj)


@admin.register(EventoAcademico)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo", "fecha", "hora_inicio", "hora_fin", "cupo_maximo", "responsable")
    search_fields = ("nombre", "tipo", "lugar", "descripcion")
    list_filter = ("tipo", "fecha")
