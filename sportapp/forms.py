from django import forms
from .models import Item, Turf, Event, Booking, EventBooking

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'category']

class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = ['name', 'location', 'type_of_sport', 'available_slots', 'price_per_hour', 'contact_info', 'rating']
        widgets = {
            'price_per_hour': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'rating': forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.1'}),
            'available_slots': forms.NumberInput(attrs={'min': '1'})
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot_time']
        widgets = {
            'slot_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBooking
        fields = ['event', 'number_of_tickets']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'location', 'date_time', 'ticket_price', 'event_details']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_details': forms.Textarea(attrs={'rows': 4}),
            'ticket_price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
        }