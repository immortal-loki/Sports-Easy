import os
import django
import datetime
from decimal import Decimal
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sports.settings')
django.setup()

# Import models after setting up Django
from sportapp.models import Item, Turf, Event, Academy, Category
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile

def add_dummy_data():
    # Get a user to use as seller
    admin_user = User.objects.get(username='admin')
    
    # Ensure all categories exist
    print("Adding categories...")
    categories = {
        'Football': Category.objects.get_or_create(name='Football')[0],
        'Cricket': Category.objects.get_or_create(name='Cricket')[0],
        'Basketball': Category.objects.get_or_create(name='Basketball')[0],
        'Tennis': Category.objects.get_or_create(name='Tennis')[0],
        'Swimming': Category.objects.get_or_create(name='Swimming')[0]
    }
    
    # Add equipment
    print("Adding equipment items...")
    equipment_data = [
        {
            'name': 'Professional Football',
            'description': 'Official size professional football with superior grip and durability.',
            'price': 1200,
            'condition': 'New',
            'category': categories['Football']
        },
        {
            'name': 'Cricket Bat',
            'description': 'Premium willow cricket bat, ideal for professional players.',
            'price': 3500,
            'condition': 'New',
            'category': categories['Cricket']
        },
        {
            'name': 'Basketball - Size 7',
            'description': 'Official size and weight basketball with excellent grip.',
            'price': 900,
            'condition': 'New',
            'category': categories['Basketball']
        },
        {
            'name': 'Tennis Racket',
            'description': 'Professional grade tennis racket, lightweight and powerful.',
            'price': 2500,
            'condition': 'New',
            'category': categories['Tennis']
        },
        {
            'name': 'Swimming Goggles',
            'description': 'Anti-fog, UV protection swimming goggles for competitive swimming.',
            'price': 500,
            'condition': 'New',
            'category': categories['Swimming']
        }
    ]
    
    for data in equipment_data:
        # Create a dummy image content (1x1 transparent pixel)
        image_content = ContentFile(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        
        # Check if item already exists
        if not Item.objects.filter(name=data['name']).exists():
            item = Item(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                seller=admin_user,
                condition=data['condition'],
                category=data['category']
            )
            item.image.save(f"{data['name'].lower().replace(' ', '_')}.png", image_content)
            item.save()
            print(f"Added equipment: {data['name']}")
    
    # Add turfs
    print("Adding turfs...")
    turf_data = [
        {
            'name': 'Green Field Soccer Turf',
            'location': 'Downtown',
            'type_of_sport': 'Football',
            'available_slots': 10,
            'price_per_hour': Decimal('800.00'),
            'contact_info': 'Phone: +91 9876543210',
            'rating': Decimal('4.5')
        },
        {
            'name': 'Cricket Stadium',
            'location': 'North Side',
            'type_of_sport': 'Cricket',
            'available_slots': 5,
            'price_per_hour': Decimal('1200.00'),
            'contact_info': 'Phone: +91 9876543211',
            'rating': Decimal('4.8')
        },
        {
            'name': 'Basketball Arena',
            'location': 'East Side',
            'type_of_sport': 'Basketball',
            'available_slots': 8,
            'price_per_hour': Decimal('600.00'),
            'contact_info': 'Phone: +91 9876543212',
            'rating': Decimal('4.2')
        },
        {
            'name': 'Tennis Court Complex',
            'location': 'West Side',
            'type_of_sport': 'Tennis',
            'available_slots': 6,
            'price_per_hour': Decimal('1000.00'),
            'contact_info': 'Phone: +91 9876543213',
            'rating': Decimal('4.7')
        },
        {
            'name': 'Multi-Sport Arena',
            'location': 'Central Park',
            'type_of_sport': 'Multiple',
            'available_slots': 15,
            'price_per_hour': Decimal('1500.00'),
            'contact_info': 'Phone: +91 9876543214',
            'rating': Decimal('4.9')
        }
    ]
    
    for data in turf_data:
        # Check if turf already exists
        if not Turf.objects.filter(name=data['name']).exists():
            turf = Turf.objects.create(
                name=data['name'],
                location=data['location'],
                type_of_sport=data['type_of_sport'],
                available_slots=data['available_slots'],
                price_per_hour=data['price_per_hour'],
                contact_info=data['contact_info'],
                rating=data['rating']
            )
            print(f"Added turf: {data['name']}")
    
    # Add events
    print("Adding events...")
    event_data = [
        {
            'name': 'Football Tournament 2024',
            'event_type': 'Tournament',
            'location': 'National Stadium',
            'date_time': timezone.now() + timezone.timedelta(days=30),
            'ticket_price': Decimal('150.00'),
            'event_details': 'Annual football tournament with teams from across the country.'
        },
        {
            'name': 'Cricket World Cup Screening',
            'event_type': 'Screening',
            'location': 'Sports Bar Arena',
            'date_time': timezone.now() + timezone.timedelta(days=15),
            'ticket_price': Decimal('100.00'),
            'event_details': 'Live screening of the Cricket World Cup finals with food and drinks.'
        },
        {
            'name': 'Basketball League Finals',
            'event_type': 'Tournament',
            'location': 'City Sports Complex',
            'date_time': timezone.now() + timezone.timedelta(days=45),
            'ticket_price': Decimal('200.00'),
            'event_details': 'The grand finale of the city basketball league.'
        },
        {
            'name': 'Tennis Masterclass',
            'event_type': 'Workshop',
            'location': 'Tennis Academy',
            'date_time': timezone.now() + timezone.timedelta(days=7),
            'ticket_price': Decimal('500.00'),
            'event_details': 'Learn from professional tennis players in this exclusive masterclass.'
        },
        {
            'name': 'Swimming Championship',
            'event_type': 'Competition',
            'location': 'Olympic Pool',
            'date_time': timezone.now() + timezone.timedelta(days=60),
            'ticket_price': Decimal('250.00'),
            'event_details': 'Annual swimming competition with categories for all age groups.'
        }
    ]
    
    for data in event_data:
        # Check if event already exists
        if not Event.objects.filter(name=data['name']).exists():
            event = Event.objects.create(
                name=data['name'],
                event_type=data['event_type'],
                location=data['location'],
                date_time=data['date_time'],
                ticket_price=data['ticket_price'],
                event_details=data['event_details']
            )
            print(f"Added event: {data['name']}")
    
    # Add academies
    print("Adding academies...")
    academy_data = [
        {
            'name': 'Elite Football Academy',
            'location': 'South City',
            'sports_offered': 'Football',
            'contact_info': 'Phone: +91 9876543220, Email: info@elitefa.com',
            'rating': Decimal('4.7')
        },
        {
            'name': 'Cricket Training Institute',
            'location': 'East End',
            'sports_offered': 'Cricket',
            'contact_info': 'Phone: +91 9876543221, Email: contact@cricketinstitute.com',
            'rating': Decimal('4.9')
        },
        {
            'name': 'Pro Basketball School',
            'location': 'North Campus',
            'sports_offered': 'Basketball',
            'contact_info': 'Phone: +91 9876543222, Email: info@probasketball.com',
            'rating': Decimal('4.5')
        },
        {
            'name': 'Tennis Excellence Center',
            'location': 'West Park',
            'sports_offered': 'Tennis',
            'contact_info': 'Phone: +91 9876543223, Email: contact@tennisexcellence.com',
            'rating': Decimal('4.8')
        },
        {
            'name': 'Aquatic Training Academy',
            'location': 'Central Lake Area',
            'sports_offered': 'Swimming, Diving, Water Polo',
            'contact_info': 'Phone: +91 9876543224, Email: info@aquaticacademy.com',
            'rating': Decimal('4.6')
        }
    ]
    
    for data in academy_data:
        # Check if academy already exists
        if not Academy.objects.filter(name=data['name']).exists():
            academy = Academy.objects.create(
                name=data['name'],
                location=data['location'],
                sports_offered=data['sports_offered'],
                contact_info=data['contact_info'],
                rating=data['rating']
            )
            print(f"Added academy: {data['name']}")
    
    print("Dummy data added successfully!")

if __name__ == '__main__':
    add_dummy_data() 