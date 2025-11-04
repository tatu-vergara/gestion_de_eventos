# eventos/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)

    organizer = models.ForeignKey(
        User, related_name="organized_events",
        on_delete=models.CASCADE
    )
    attendees = models.ManyToManyField(
        User, related_name="attending_events", blank=True
    )
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", args=[self.pk])


    class Meta:
        permissions = [
            ("can_edit_event", "Can edit event (organizer/admin)"),
            ("can_view_private_event", "Can view private event"),
        ]

    def __str__(self):
        return self.title
