from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from eventos.models import Event

class Command(BaseCommand):
    help = "Crea grupos y asigna permisos para Administradores, Organizadores y Asistentes."

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Event)

        perms = {
            "add_event": Permission.objects.get(codename="add_event", content_type=content_type),
            "change_event": Permission.objects.get(codename="change_event", content_type=content_type),
            "delete_event": Permission.objects.get(codename="delete_event", content_type=content_type),
            "view_event": Permission.objects.get(codename="view_event", content_type=content_type),
            "can_edit_event": Permission.objects.get(codename="can_edit_event", content_type=content_type),
            "can_view_private_event": Permission.objects.get(codename="can_view_private_event", content_type=content_type),
        }

        admin_group, _ = Group.objects.get_or_create(name="Administradores")
        organizer_group, _ = Group.objects.get_or_create(name="Organizadores")
        attendee_group, _ = Group.objects.get_or_create(name="Asistentes")

        # Admin: todos los permisos del modelo Event
        admin_group.permissions.set(perms.values())

        # Organizadores: no delete
        organizer_group.permissions.set([
            perms["add_event"],
            perms["change_event"],
            perms["view_event"],
            perms["can_edit_event"],
            perms["can_view_private_event"],
        ])

        # Asistentes: ver (el detalle de privados depende de la lógica o permiso extra)
        attendee_group.permissions.set([
            perms["view_event"],
        ])

        self.stdout.write(self.style.SUCCESS("Grupos y permisos inicializados."))
