from django.utils import timezone
from .models import Appointment
from django.db import transaction
from django.db.models import Q

def check_availability(start_time, end_time):
    """
    Checks if the given time slot is available.
    Returns True if available, False otherwise.
    """
    # Simple overlap check:
    # (StartA < EndB) and (EndA > StartB)
    overlapping = Appointment.objects.filter(
        Q(start_time__lt=end_time) & Q(end_time__gt=start_time),
        status__in=['PENDING', 'CONFIRMED']
    ).exists()
    
    return not overlapping

def create_appointment(user, start_time, end_time, session_type):
    """
    Creates an appointment if the slot is available.
    Returns the appointment object or None if unavailable.
    """
    with transaction.atomic():
        if check_availability(start_time, end_time):
            appointment = Appointment.objects.create(
                user=user,
                start_time=start_time,
                end_time=end_time,
                session_type=session_type,
                status='PENDING' # Default to pending confirmation
            )
            return appointment
    return None

def get_user_appointments(user):
    """
    Returns all appointments for a specific user, ordered by start time.
    """
    return Appointment.objects.filter(user=user).order_by('-start_time')
