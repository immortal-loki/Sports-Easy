from django.contrib import admin
from .models import Item, Turf, Event, Academy, Comment, Category, Booking, AcademyAdmission, EventBooking
# Register your models here.
# marketplace/admin.py

class AcademyAdmissionAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'academy', 'sport', 'email', 'phone', 'fee', 'date_admitted')
    list_filter = ('academy', 'sport', 'date_admitted')
    search_fields = ('student_name', 'email', 'phone')
    readonly_fields = ('date_admitted',)

admin.site.register(Item)
admin.site.register(Turf)
admin.site.register(Event)
admin.site.register(Academy)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(EventBooking)
admin.site.register(AcademyAdmission, AcademyAdmissionAdmin)