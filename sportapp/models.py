from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): 
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.name

class Turf(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type_of_sport = models.CharField(max_length=100)
    available_slots = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    contact_info = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)


    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    slot_time = models.DateTimeField()
    duration = models.IntegerField()  

    def __str__(self):
        return f"Booking for {self.turf.name} by {self.user.username}"

class Event(models.Model):
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    event_details = models.TextField()

    def __str__(self):
        return self.name

class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.event.name} by {self.user.username}"

class Academy(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    sports_offered = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

class AcademyAdmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    sport = models.CharField(max_length=100)
    experience = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    date_admitted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student_name}'s admission to {self.academy.name} for {self.sport}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment on {self.post.title}"



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} ({'User' if self.user else 'Guest'})"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())