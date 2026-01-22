from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from openai import OpenAI
from .models import Appointment
from .services import create_appointment, get_user_appointments
from .forms import BookingForm

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def home(request: HttpRequest):
  return render(request, "core/home.html")


def how_it_works(request: HttpRequest):
  return render(request, "core/how_it_works.html")

def what_makes_us_different(request: HttpRequest):
    return render(request, "core/what_makes_us_different.html")

def your_journey(request: HttpRequest):
    return render(request, "core/your_journey.html")

def about(request: HttpRequest):
    return render(request, "core/aboutus.html")

def psycho_education(request: HttpRequest):
    return render(request, "core/pea.html")

def resources(request: HttpRequest):
    return render(request, "core/resources.html")

def contact(request: HttpRequest):
    return render(request, "core/contact.html")

def privacy_policy(request: HttpRequest):
    return render(request, "core/legal/privacy.html")

def refund_policy(request: HttpRequest):
    return render(request, "core/legal/refund.html")
    
def confidentiality_policy(request: HttpRequest):
    return render(request, "core/legal/confidentiality.html")

@login_required
def booking_view(request: HttpRequest):
    from datetime import datetime, timedelta, time
    
    # Generate slots for the next 14 days
    today = datetime.now().date()
    slots_data = {} # { "2023-10-27": [datetime objects] }
    
    for i in range(1, 15):
        day = today + timedelta(days=i)
        day_str = day.strftime("%A, %b %d") # e.g. "Monday, Oct 27"
        day_slots = []
        
        # Logic: Weekday vs Weekend
        if day.weekday() < 5: # Mon(0) - Fri(4)
            # Weekdays: Evening slots 5 PM - 8 PM
            hours = [17, 18, 19, 20]
        else: # Sat(5) - Sun(6)
            # Weekends: All day 10 AM - 6 PM
            hours = [10, 11, 12, 14, 15, 16, 17, 18]
            
        for h in hours:
            # Create a localized datetime or naive if using simplified
            slot_dt = datetime.combine(day, time(hour=h))
            day_slots.append(slot_dt)
            
        if day_slots:
            slots_data[day_str] = day_slots

    if request.method == 'POST':
        # We expect 'slot_time' string from the clicked button
        slot_str = request.POST.get('slot_time')
        session_type = request.POST.get('session_type', 'online')
        
        if slot_str:
            try:
                # Parse the ISO format string back to datetime
                start_time = datetime.fromisoformat(slot_str)
                end_time = start_time + timedelta(hours=1)
                
                appointment = create_appointment(request.user, start_time, end_time, session_type)
                if appointment:
                    messages.success(request, f"Confirmed! Your session is booked for {start_time.strftime('%A, %b %d at %I:%M %p')}.")
                    return redirect('history')
                else:
                    messages.error(request, "That slot was just taken. Please pick another.")
            except ValueError:
                messages.error(request, "Invalid time format.")
        else:
            messages.error(request, "Please select a time slot.")

    return render(request, "core/booking.html", {'slots_data': slots_data})

@login_required
def history_view(request: HttpRequest):
    appointments = get_user_appointments(request.user)
    return render(request, "core/history.html", {'appointments': appointments})

def chatbot_reply(request: HttpRequest):
  if request.method != "POST":
    return JsonResponse({"error": "POST required"}, status=405)

  user_message = request.POST.get("message", "")[:500]
  if not user_message:
    return JsonResponse({"reply": "Please type something so I can help."})
    
  # Simple rule-based fallback if API key is missing or connection fails
  api_key = os.environ.get("OPENAI_API_KEY")
  
  if not api_key:
      # Fallback logic
      msg = user_message.lower()
      if "book" in msg or "appointment" in msg or "schedule" in msg:
          text = "You can book a session by visiting our <a href='/booking/'>Booking Page</a>. We offer flexible slots for weekdays and weekends."
      elif "log" in msg or "sign" in msg:
          text = "You can log in to your account <a href='/signin/'>here</a> to verify your history or access resources."
      elif "hello" in msg or "hi " in msg:
          text = "Hello! I am your MindSettler guide. How can I help you today?"
      elif "work" in msg:
          text = "We offer structured therapy sessions. You can learn more on our <a href='/how-it-works/'>Flow</a> page."
      else:
          text = "I'm currently in offline mode, but I'm here to help. You can explore our services using the menu above, or book a session directly."
      
      return JsonResponse({"reply": text})

  try:
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "system",
          "content": (
            "You are a gentle website guide for MindSettler, a psycho‑education "
            "and therapy platform in India. Explain services, sessions, and "
            "booking in a calm, human tone. Never give crisis, diagnostic, or "
            "medication advice. If the user asks about 'how it works', "
            "or 'booking', direct them to the booking page."
          ),
        },
        {"role": "user", "content": user_message},
      ],
    )
    text = completion.choices[0].message.content.strip()
  except Exception:
    text = "Sorry, something went wrong while talking to the assistant. Please try again later."

  return JsonResponse({"reply": text})


from django.contrib.auth import authenticate, login

def signin(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Try to authenticate with username as email (since custom user model or if username field is used as email)
        # Note: Standard django allows username auth. If user puts email in username field, this works.
        # But if we need email auth specifically, we might need a backend or query user by email.
        # Let's assume username=email for now or try both.
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully signed in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
            
    return render(request, "core/signin.html")
