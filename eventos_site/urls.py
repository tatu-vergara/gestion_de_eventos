# eventos_site/eventos_site/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import handler403
from eventos import views as ev

urlpatterns = [
    path("admin/", admin.site.urls),

    # Vistas de eventos
    path("", ev.EventListView.as_view(), name="event_list"),
    path("eventos/nuevo/", ev.EventCreateView.as_view(), name="event_create"),
    path("eventos/<int:pk>/", ev.EventDetailView.as_view(), name="event_detail"),
    path("eventos/<int:pk>/editar/", ev.EventUpdateView.as_view(), name="event_update"),
    path("eventos/<int:pk>/eliminar/", ev.EventDeleteView.as_view(), name="event_delete"),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]

handler403 = ev.permission_denied_view