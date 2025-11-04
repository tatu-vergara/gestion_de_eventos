# eventos/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import EventForm
from .models import Event

def user_can_view_event(user, event: Event) -> bool:
    if not event.is_private:
        return True
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if user.has_perm("eventos.can_view_private_event"):
        return True
    if event.organizer_id == user.id:
        return True
    if event.attendees.filter(id=user.id).exists():
        return True
    return False

class EventListView(ListView):
    model = Event
    template_name = "eventos/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        qs = Event.objects.all().select_related("organizer")
        user = self.request.user
        if user.is_authenticated and (user.is_superuser or user.has_perm("eventos.can_view_private_event")):
            return qs
        # Usuarios no autorizados a privados ven solo públicos o donde participan
        if user.is_authenticated:
            # Ve públicos + los que organiza + a los que asiste
            return qs.filter(
                Q(is_private=False) |
                Q(organizer=user) |
                Q(attendees=user)
            )
        return qs.filter(is_private=False)

class EventDetailView(DetailView):
    model = Event
    template_name = "eventos/event_detail.html"
    context_object_name = "event"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not user_can_view_event(request.user, obj):
            messages.error(request, "No tienes permisos para ver este evento (es privado).")
            raise PermissionDenied("Acceso denegado a evento privado")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.request.user
        e = self.object

        can_edit = (
            u.is_authenticated and (
                u.is_superuser or (
                    e.organizer_id == u.id and u.has_perm("eventos.can_edit_event")
                )
            )
        )
        can_delete = u.is_authenticated and u.is_superuser  # solo admin

        ctx["can_edit"] = can_edit
        ctx["can_delete"] = can_delete
        return ctx

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/event_form.html"


    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Evento creado con éxito.")
        return super().form_valid(form)

class EventUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/event_form.html"
    success_url = reverse_lazy("event_list")
    permission_required = ("eventos.can_edit_event",)
    raise_exception = True   # lanzará 403 en vez de redirigir a login
    permission_denied_message = "No tienes permisos para editar este evento."

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # además del permiso global, exigimos ser organizador o superuser
        if not (request.user.is_superuser or obj.organizer_id == request.user.id):
            messages.error(request, "Solo el organizador o admin puede editar este evento.")
            raise PermissionDenied("No autorizado para editar este evento.")
        return super().dispatch(request, *args, **kwargs)

class EventDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "eventos/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")
    # En tu consigna: solo administradores (superuser) pueden eliminar.
    permission_required = ("eventos.delete_event",)
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Solo administradores pueden eliminar eventos.")
            raise PermissionDenied("No autorizado para eliminar.")
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render

def permission_denied_view(request, exception):
    messages.error(request, "Acceso denegado: no tienes permisos suficientes.")
    return render(request, "403.html", status=403)