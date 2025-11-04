from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "is_private", "attendees"]
        widgets = {
            # Opción A: datetime-local (un solo input con fecha+hora)
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    # Necesario para que Django parsee el formato del widget
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].input_formats = ["%Y-%m-%dT%H:%M"]
