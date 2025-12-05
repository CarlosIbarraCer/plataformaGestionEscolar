import random
import string
import base64
from django.contrib.auth.models import Group, Permission

ROLE_PERMISSIONS = {
    "maestro": ["view_alumnos", "change_alumnos", "delete_alumnos", "view_eventoacademico"],
    "administrador": [
        "view_alumnos",
        "change_alumnos",
        "delete_alumnos",
        "view_maestros",
        "change_maestros",
        "delete_maestros",
        "add_eventoacademico",
        "change_eventoacademico",
        "delete_eventoacademico",
        "view_eventoacademico",
    ],
}


def ensure_role_permissions(role_name: str) -> Group:
    """
    Make sure each role's group exists and carries the minimum permissions.
    Idempotent so it can be called every time a user is created/updated.
    """
    normalized = (role_name or "").lower()
    group, _ = Group.objects.get_or_create(name=normalized)
    required_codenames = ROLE_PERMISSIONS.get(normalized, [])
    if required_codenames:
        perms = Permission.objects.filter(
            content_type__app_label="dev_sistema_escolar_api",
            codename__in=required_codenames,
        )
        group.permissions.add(*perms)
    return group

class Utils:

    @staticmethod
    def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    @staticmethod
    def randomNumber(numberLength=10):
        """Generate a random number of fixed length """
        digits = string.digits
        return ''.join(random.choice(digits) for i in range(numberLength))

    @staticmethod
    def requestRawFileToB64(file):
        file_b64 = str(base64.b64encode(file.read()).decode())
        return file_b64

    @staticmethod
    def mimeFromFilename(filename):
        content_type = ""
        if '.mp4' in filename:
            content_type = "video/mp4"
        elif '.m4v' in filename:
            content_type = "video/mp4"
        else:
            content_type = "application/octet-stream"
        
        return content_type

    @staticmethod
    def requestFileToB64(logo):

        content_type = ""
        if '.jpg' in logo.name or '.jpeg' in logo.name:
            content_type = "data:image/jpeg;base64,"
        elif '.png' in logo.name:
            content_type = "data:image/png;base64,"

        logo_b64 = content_type+str(base64.b64encode(logo.read()).decode())

        return logo_b64
