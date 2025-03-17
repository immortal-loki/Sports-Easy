from django.shortcuts import render, redirect, get_object_or_404
from.models import Item, Turf, Event, Academy, Comment, Category, Booking, Cart, EventBooking, AcademyAdmission
from.forms import ItemForm, BookingForm, EventBookingForm ,TurfForm, EventForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
import json
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item_create.html', {'form': form})

@login_required
def turf_create(request):
    if request.method == 'POST':
        form = TurfForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('turf_list')
    else:
        form = TurfForm()
    return render(request, 'turf_create.html', {'form': form})

def turf_list(request):
    location = request.GET.get('location', '')
    if location:
        turfs = Turf.objects.filter(location__icontains=location)
    else:
        turfs = Turf.objects.all()
    return render(request, 'turf_list.html', {'turfs': turfs, 'location': location})

@login_required
def turf_booking(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.turf = turf
            booking.duration = 1  # Set fixed duration to 1 hour
            
            # Get the requested time slot
            requested_time = booking.slot_time
            
            # Check if this exact time slot is already booked
            existing_booking = Booking.objects.filter(
                turf=turf,
                slot_time=requested_time
            ).first()
            
            if existing_booking:
                # Get the next available time slot (1 hour after the existing booking)
                next_available = existing_booking.slot_time + timezone.timedelta(hours=1)
                messages.error(request, f'This time slot is already booked. The next available slot is at {next_available.strftime("%I:%M %p")}.')
                return render(request, 'turf_booking.html', {'form': form, 'turf': turf})
            
            # Store booking details in session for payment processing
            request.session['turf_booking'] = {
                'turf_id': turf.id,
                'slot_time': booking.slot_time.isoformat(),
                'total_amount': float(turf.price_per_hour)  # One hour booking
            }
            
            return redirect('checkout')
    else:
        form = BookingForm()
    return render(request, 'turf_booking.html', {'form': form, 'turf': turf})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

@login_required
def event_booking(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        number_of_tickets = int(request.POST.get('number_of_tickets', 1))
        total_amount = float(event.ticket_price * number_of_tickets)
        
        # Store booking details in session for payment processing
        request.session['event_booking'] = {
            'event_id': event.id,
            'number_of_tickets': number_of_tickets,
            'total_amount': total_amount,
            'event_name': event.name,
            'ticket_price': float(event.ticket_price)
        }
        
        return redirect('checkout')
    return render(request, 'event_booking.html', {'event': event})

def academy_list(request):
    academies = Academy.objects.all()
    return render(request, 'academy_list.html', {'academies': academies})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'comments.html', {'post': post, 'comments': comments})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
            
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
        
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def equipment_list(request):
    return render(request, 'equipment_list.html')

def turf_booked(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        context = {
            'booking': booking,
            'total_amount': booking.turf.price_per_hour * booking.duration
        }
        return render(request, 'turf_booked.html', context)
    except Booking.DoesNotExist:
        messages.error(request, 'The booking you are looking for does not exist.')
        return render(request, 'error.html', {
            'message': 'The booking you are looking for does not exist. Please check your booking history or contact support.'
        })
    except Exception as e:
        messages.error(request, 'An error occurred while retrieving your booking.')
        return render(request, 'error.html', {
            'message': 'An unexpected error occurred. Please try again later or contact support.'
        })

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = request.session.get('cart', {})
    
    if str(item.id) in cart:
        cart[str(item.id)]['quantity'] += 1
    else:
        cart[str(item.id)] = {'name': item.name, 'price': item.price, 'quantity': 1, 'image': item.image.url}
    
    request.session['cart'] = cart
    messages.success(request, f'{item.name} added to cart successfully!')
    return redirect('item_list')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for item_id, item_data in cart.items():
        item_data['id'] = item_id
        cart_items.append(item_data)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    # Get booking details from session
    turf_booking = request.session.get('turf_booking')
    event_booking = request.session.get('event_booking')
    cart = request.session.get('cart', {})
    
    if turf_booking:
        turf = get_object_or_404(Turf, id=turf_booking['turf_id'])
        context = {
            'turf': turf,
            'slot_time': turf_booking['slot_time'],
            'total_amount': turf_booking['total_amount'],
            'booking_type': 'turf'
        }
        return render(request, 'checkout.html', context)
    elif event_booking:
        event = get_object_or_404(Event, id=event_booking['event_id'])
        context = {
            'event': event,
            'number_of_tickets': event_booking['number_of_tickets'],
            'total_amount': event_booking['total_amount'],
            'booking_type': 'event'
        }
        return render(request, 'checkout.html', context)
    elif cart:
        # Process cart items for checkout
        cart_items = []
        total_amount = 0
        for item_id, item_data in cart.items():
            item_data['id'] = item_id
            item_data['subtotal'] = item_data['price'] * item_data['quantity']
            total_amount += item_data['subtotal']
            cart_items.append(item_data)
        
        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'booking_type': 'cart'
        }
        return render(request, 'checkout.html', context)
    else:
        messages.error(request, 'No items found in cart or booking. Please try again.')
        return redirect('home')

@login_required
def process_payment(request):
    # Ensure we're dealing with a POST request
    if request.method != 'POST':
        messages.error(request, 'Invalid request method. This page requires a POST request.')
        return redirect('home')
        
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register to complete your purchase.')
        return redirect('login')
    
    # Get booking details from session
    turf_booking = request.session.get('turf_booking')
    event_booking = request.session.get('event_booking')
    academy_admission = request.session.get('academy_admission')
    cart = request.session.get('cart', {})
    
    # Debug logging
    print(f"[DEBUG] Processing payment. Session data:")
    print(f"[DEBUG] - turf_booking: {turf_booking}")
    print(f"[DEBUG] - event_booking: {event_booking}")
    print(f"[DEBUG] - academy_admission: {academy_admission}")
    print(f"[DEBUG] - cart items: {len(cart)}")
    
    # Simple payment validation (in real-world, you'd validate card info)
    card_name = request.POST.get('card_name')
    card_number = request.POST.get('card_number')
    expiry = request.POST.get('expiry')
    cvv = request.POST.get('cvv')
    
    if not all([card_name, card_number, expiry, cvv]):
        messages.error(request, 'Please fill in all payment details.')
        return redirect('checkout')
    
    try:
        # Process cart checkout
        if cart:
            print("[DEBUG] Processing cart payment")
            request.session['cart'] = {}
            request.session.save()  # Explicitly save the session
            messages.success(request, 'Payment successful! Your order has been placed.')
            return redirect('item_list')
        
        # Process turf booking
        elif turf_booking:
            print("[DEBUG] Processing turf booking payment")
            turf = get_object_or_404(Turf, id=turf_booking['turf_id'])
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                turf=turf,
                slot_time=turf_booking['slot_time'],
                duration=1
            )
            
            # Clear session data
            del request.session['turf_booking']
            request.session.save()  # Explicitly save the session
            
            messages.success(request, 'Payment successful! Your turf has been booked.')
            return redirect('turf_booked', booking_id=booking.id)
        
        # Process event booking
        elif event_booking:
            print("[DEBUG] Processing event booking payment")
            # Make sure we can get the event
            event_id = event_booking.get('event_id')
            if not event_id:
                messages.error(request, 'Invalid event booking data.')
                return redirect('event_list')
            
            # Get event and create booking
            try:
                event = Event.objects.get(id=event_id)
                booking = EventBooking.objects.create(
                    user=request.user,
                    event=event,
                    number_of_tickets=event_booking['number_of_tickets']
                )
                
                print(f"[DEBUG] Created event booking: {booking.id}")
                
                # Save message data before clearing session
                num_tickets = event_booking['number_of_tickets']
                event_name = event.name
                
                # Clear session data
                del request.session['event_booking']
                request.session.save()  # Explicitly save the session
                
                # Set success message and redirect
                messages.success(request, f'Payment successful! Your {num_tickets} ticket(s) for {event_name} have been booked.')
                return redirect('event_list')
            
            except Event.DoesNotExist:
                messages.error(request, 'The event you are trying to book does not exist.')
                return redirect('event_list')
            
            except Exception as event_error:
                print(f"[DEBUG] Event booking error: {str(event_error)}")
                messages.error(request, f'Error processing event booking: {str(event_error)}')
                return redirect('checkout')
        
        # Process academy admission
        elif academy_admission:
            print("[DEBUG] Processing academy admission payment")
            academy_id = academy_admission.get('academy_id')
            if not academy_id:
                messages.error(request, 'Invalid academy admission data.')
                return redirect('academy_list')
            
            try:
                academy = Academy.objects.get(id=academy_id)
                
                # Here you would typically create an academy admission record
                # For now, we'll just process the payment
                
                # Save data before clearing session
                academy_name = academy.name
                sport = academy_admission['sport']
                student_name = academy_admission['student_name']
                email = academy_admission['email']
                phone = academy_admission['phone']
                experience = int(academy_admission['experience'])
                message = academy_admission['message']
                fee = float(academy_admission['fee'])
                
                # Create AcademyAdmission record
                admission = AcademyAdmission.objects.create(
                    user=request.user,
                    academy=academy,
                    student_name=student_name,
                    email=email,
                    phone=phone,
                    sport=sport,
                    experience=experience,
                    message=message,
                    fee=fee
                )
                
                print(f"[DEBUG] Created academy admission record: {admission.id}")
                
                # Clear session data
                del request.session['academy_admission']
                request.session.save()
                
                # Set success message and redirect
                messages.success(request, f'Payment successful! {student_name}\'s admission to {academy_name} for {sport} has been processed. Welcome to the academy!')
                
                # Store the admission ID in session for the completion page
                request.session['last_admission_id'] = admission.id
                request.session.save()
                
                return redirect('academy_admission_complete')
            
            except Academy.DoesNotExist:
                messages.error(request, 'The academy you are applying to does not exist.')
                return redirect('academy_list')
            
            except Exception as academy_error:
                print(f"[DEBUG] Academy admission error: {str(academy_error)}")
                messages.error(request, f'Error processing academy admission: {str(academy_error)}')
                return redirect('academy_checkout')
        
        # No valid booking found
        else:
            messages.error(request, 'No items found to process payment. Your session may have expired.')
            return redirect('home')
            
    except Exception as e:
        print(f"[DEBUG] Payment processing error: {str(e)}")
        messages.error(request, f'An error occurred during payment processing: {str(e)}')
        return redirect('checkout')

def update_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart[str(item_id)]['quantity'] = quantity
            request.session['cart'] = cart
            messages.success(request, 'Cart updated successfully!')
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart successfully!')
    return redirect('cart')

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})

def academy_detail(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id)
    return render(request, 'academy_detail.html', {'academy': academy})

@login_required
def academy_admission(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id)
    if request.method == 'POST':
        # Get all form fields
        student_name = request.POST.get('student_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        sport = request.POST.get('sport', '')
        experience = request.POST.get('experience', '')
        message = request.POST.get('message', '')
        
        # Store admission details in session
        admission_fee = 199.99  # Sample admission fee
        request.session['academy_admission'] = {
            'academy_id': academy.id,
            'academy_name': academy.name,
            'student_name': student_name,
            'email': email,
            'phone': phone,
            'sport': sport,
            'experience': experience,
            'message': message,
            'fee': float(admission_fee)
        }
        
        return redirect('academy_checkout')
    return render(request, 'academy_admission.html', {'academy': academy})

@login_required
def academy_checkout(request):
    # Get academy admission details from session
    academy_admission = request.session.get('academy_admission')
    
    if not academy_admission:
        messages.error(request, 'No academy admission details found. Please start over.')
        return redirect('academy_list')
    
    academy = get_object_or_404(Academy, id=academy_admission['academy_id'])
    
    context = {
        'academy': academy,
        'admission': academy_admission,
        'total_amount': academy_admission['fee'],
        'booking_type': 'academy'
    }
    
    return render(request, 'checkout.html', context)

def academy_admission_complete(request):
    admission_id = request.session.get('last_admission_id')
    admission = None
    
    if admission_id:
        try:
            admission = AcademyAdmission.objects.get(id=admission_id)
            # Clear the session data after retrieving
            del request.session['last_admission_id']
            request.session.save()
        except AcademyAdmission.DoesNotExist:
            pass
    
    return render(request, 'academy_admission_complete.html', {'admission': admission})