from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import Room, Guest, Booking


# =========================
# HOME / DASHBOARD
# =========================

@login_required
def home(request):
    rooms = Room.objects.all()
    available_rooms = Room.objects.filter(status='Available').count()
    booked_rooms = Room.objects.filter(status='Booked').count()
    maintenance_rooms = Room.objects.filter(status='Maintenance').count()
    cancelled_bookings = Booking.objects.filter(status='Cancelled').count()
    completed_bookings = Booking.objects.filter(status='Completed').count()
    guests = Guest.objects.all()
    bookings = Booking.objects.all()
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    total_revenue = sum(
    booking.total_amount
    for booking in Booking.objects.filter(status='Booked')
   
)
    total_revenue = sum(
    booking.total_amount
    for booking in Booking.objects.filter(
        status__in=['Booked', 'Completed']
    )
)

    context = {
        'rooms': rooms,
        'guests': guests,
        'bookings': bookings,
        'available_rooms': available_rooms,
        'cancelled_bookings': cancelled_bookings,
        'completed_bookings': completed_bookings,        'total_revenue': total_revenue,
        'booked_rooms': booked_rooms,
        'maintenance_rooms': maintenance_rooms,

    }

    return render(request, 'hotel/home.html', context)


# =========================
# ROOM SEARCH
# =========================

@login_required
def rooms(request):
    search = request.GET.get('search', '').strip()

    rooms = Room.objects.filter(
        room_number__icontains=search
    )

    return render(request, 'hotel/rooms.html', {
        'rooms': rooms,
        'search': search,
    })


# =========================
# GUEST SEARCH
# =========================

@login_required
def guests(request):
    search = request.GET.get('search', '').strip()

    guests = Guest.objects.filter(
        name__icontains=search
    )

    return render(request, 'hotel/guests.html', {
        'guests': guests,
        'search': search,
    })


# =========================
# BOOKINGS
# =========================

@login_required
def bookings(request):

    # -------------------------
    # ADD BOOKING
    # -------------------------

    if request.method == 'POST':

        guest_id = request.POST.get('guest')
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        check_in_date = datetime.strptime(
            check_in, '%Y-%m-%d'
        ).date()

        check_out_date = datetime.strptime(
            check_out, '%Y-%m-%d'
        ).date()

        # Date validation
        if check_out_date <= check_in_date:
            messages.error(
                request,
                'Check-out date must be after check-in date.'
            )
            return redirect('/bookings/')

        room = Room.objects.get(id=room_id)

        # Room availability
        if room.status != 'Available':
            messages.error(
                request,
                'This room is not available.'
            )
            return redirect('/bookings/')

        # Calculate total amount
        days = (check_out_date - check_in_date).days
        total_amount = room.price * days

        # Create booking
        Booking.objects.create(
            guest_id=guest_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            total_amount=total_amount
        )

        # Change room status
        room.status = 'Booked'
        room.save()

        messages.success(
            request,
            'Booking created successfully.'
        )

        return redirect('/bookings/')

    # -------------------------
    # SEARCH & FILTER BOOKING
    # -------------------------

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    bookings = Booking.objects.all().order_by('-created_at')

    # Search by guest name OR room number
    if search:
        from django.db.models import Q

        bookings = bookings.filter(
            Q(guest__name__icontains=search) |
            Q(room__room_number__icontains=search)
        )

    # Filter by booking status
    if status:
        bookings = bookings.filter(
            status=status
        )

    guests = Guest.objects.all()
    rooms = Room.objects.filter(status='Available')

    return render(request, 'hotel/bookings.html', {
        'bookings': bookings,
        'guests': guests,
        'rooms': rooms,
        'search': search,
        'status': status,
    })


# =========================
# ROOM CRUD
# =========================

@login_required
def add_room(request):

    if request.method == 'POST':

        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        price = request.POST.get('price')
        status = request.POST.get('status')

        Room.objects.create(
            room_number=room_number,
            room_type=room_type,
            price=price,
            status=status
        )

        return redirect('/rooms/')

    return render(request, 'hotel/add_room.html')


@login_required
def edit_room(request, room_id):

    room = Room.objects.get(id=room_id)

    if request.method == 'POST':

        room.room_number = request.POST.get('room_number')
        room.room_type = request.POST.get('room_type')
        room.price = request.POST.get('price')
        room.status = request.POST.get('status')

        room.save()

        return redirect('/rooms/')

    return render(
        request,
        'hotel/edit_room.html',
        {'room': room}
    )


@login_required
def delete_room(request, room_id):

    room = Room.objects.get(id=room_id)
    room.delete()

    return redirect('/rooms/')


# =========================
# GUEST CRUD
# =========================

@login_required
def add_guest(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        Guest.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )

        return redirect('/guests/')

    return render(request, 'hotel/add_guest.html')


@login_required
def edit_guest(request, guest_id):

    guest = Guest.objects.get(id=guest_id)

    if request.method == 'POST':

        guest.name = request.POST.get('name')
        guest.phone = request.POST.get('phone')
        guest.email = request.POST.get('email')
        guest.address = request.POST.get('address')

        guest.save()

        return redirect('/guests/')

    return render(
        request,
        'hotel/edit_guest.html',
        {'guest': guest}
    )


@login_required
def delete_guest(request, guest_id):

    if request.method == 'POST':

        guest = Guest.objects.get(id=guest_id)
        guest.delete()

    return redirect('/guests/')


# =========================
# CANCEL BOOKING
# =========================

@login_required
def cancel_booking(request, booking_id):

    if request.method == 'POST':

        booking = Booking.objects.get(id=booking_id)

        booking.status = 'Cancelled'
        booking.save()

        room = booking.room
        room.status = 'Available'
        room.save()

        messages.success(
            request,
            'Booking cancelled successfully.'
        )

    return redirect('/bookings/')
# =========================
# COMPLETE BOOKING
# =========================

@login_required
def complete_booking(request, booking_id):

    if request.method == 'POST':

        booking = Booking.objects.get(id=booking_id)

        booking.status = 'Completed'
        booking.save()

        room = booking.room
        room.status = 'Available'
        room.save()

        messages.success(
            request,
            'Booking completed successfully.'
        )

    return redirect('/bookings/')


# =========================
# BOOKING HISTORY
# =========================

@login_required
def booking_history(request):

    status = request.GET.get('status', '').strip()

    bookings = Booking.objects.all().order_by('-created_at')

    if status:
        bookings = bookings.filter(
            status=status
        )

    return render(
        request,
        'hotel/booking_history.html',
        {
            'bookings': bookings,
            'status': status,
        }
    )
# =========================
# INVOICE
# =========================

@login_required
def invoice(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    return render(
        request,
        'hotel/invoice.html',
        {
            'booking': booking,
        }
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'hotel/login.html'
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect('/login/')
@login_required
def gallery(request):
    return render(request, 'hotel/gallery.html')

